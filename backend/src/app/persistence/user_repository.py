from typing import Any, TypeVar

from sqlalchemy import ColumnElement, Select, String, UnaryExpression, cast, func, or_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain.pagination import Page, SortDirection
from app.domain.queries import UserQuery, UserSortField
from app.domain.text import phone_search_digits
from app.domain.user import User
from app.persistence.models import UserRecord

StatementT = TypeVar("StatementT", bound=Select[Any])

SORT_COLUMNS = {
    UserSortField.ID: UserRecord.id,
    UserSortField.NAME: UserRecord.name,
    UserSortField.USERNAME: UserRecord.username,
    UserSortField.EMAIL: UserRecord.email,
}


class PostgresUserRepository:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def find(self, user_id: int) -> User | None:
        async with self._session_factory() as session:
            record = await session.get(UserRecord, user_id)
            return _to_domain(record) if record is not None else None

    async def save(self, user: User) -> None:
        mutable_columns = {
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "fetched_at": func.now(),
        }
        statement = (
            insert(UserRecord)
            .values(id=user.id, **mutable_columns)
            .on_conflict_do_update(index_elements=[UserRecord.id], set_=mutable_columns)
        )
        async with self._session_factory() as session, session.begin():
            await session.execute(statement)

    async def search(self, query: UserQuery) -> Page[User]:
        async with self._session_factory() as session:
            total = await session.scalar(
                _apply_search(select(func.count()).select_from(UserRecord), query)
            )
            records = await session.scalars(
                _apply_search(select(UserRecord), query)
                .order_by(_order_by(query))
                .limit(query.page_size)
                .offset(query.offset)
            )
            return Page(
                items=[_to_domain(record) for record in records],
                total=total or 0,
                page=query.page,
                page_size=query.page_size,
            )


def _apply_search(statement: StatementT, query: UserQuery) -> StatementT:
    if not query.search:
        return statement

    pattern = f"%{query.search}%"
    conditions: list[ColumnElement[bool]] = [
        cast(UserRecord.id, String).ilike(pattern),
        UserRecord.name.ilike(pattern),
        UserRecord.username.ilike(pattern),
        UserRecord.email.ilike(pattern),
    ]

    digits = phone_search_digits(query.search)
    if digits is not None:
        conditions.append(UserRecord.phone.ilike(f"%{digits}%"))

    return statement.where(or_(*conditions))


def _order_by(query: UserQuery) -> UnaryExpression[Any]:
    column = SORT_COLUMNS[query.sort_by]
    return column.desc() if query.sort_direction is SortDirection.DESC else column.asc()


def _to_domain(record: UserRecord) -> User:
    return User(
        id=record.id,
        name=record.name,
        username=record.username,
        email=record.email,
        phone=record.phone,
    )
