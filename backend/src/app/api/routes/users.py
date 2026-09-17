from typing import Annotated, Any

from fastapi import APIRouter, Query, status

from app.api import docs
from app.api.dependencies import FetchUsersServiceDep, ListUsersServiceDep
from app.api.schemas import (
    ErrorResponse,
    FetchUsersRequest,
    FetchUsersResponse,
    ListUsersParams,
    UserPageResponse,
)

router = APIRouter(prefix="/users", tags=["users"])

ERROR_RESPONSES: dict[int | str, dict[str, Any]] = {
    422: {"model": ErrorResponse, "description": "Entrada inválida."},
    500: {"model": ErrorResponse, "description": "Falha interna do serviço."},
}


@router.post(
    "/fetch",
    response_model=FetchUsersResponse,
    status_code=status.HTTP_200_OK,
    summary=docs.FETCH_USERS_SUMMARY,
    description=docs.FETCH_USERS_DESCRIPTION,
    response_description="Usuários resolvidos e IDs que falharam.",
    responses=ERROR_RESPONSES,
)
async def fetch_users(
    payload: FetchUsersRequest, service: FetchUsersServiceDep
) -> FetchUsersResponse:
    result = await service.execute(payload.user_ids)
    return FetchUsersResponse.from_result(result)


@router.get(
    "",
    response_model=UserPageResponse,
    status_code=status.HTTP_200_OK,
    summary=docs.LIST_USERS_SUMMARY,
    description=docs.LIST_USERS_DESCRIPTION,
    response_description="Página de usuários já resolvidos.",
    responses=ERROR_RESPONSES,
)
async def list_users(
    params: Annotated[ListUsersParams, Query()], service: ListUsersServiceDep
) -> UserPageResponse:
    page = await service.execute(params.to_query())
    return UserPageResponse.from_page(page)
