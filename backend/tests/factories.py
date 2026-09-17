from app.domain.user import User


def build_user(user_id: int, phone: str | None = "11987654321") -> User:
    return User(
        id=user_id,
        name=f"User {user_id}",
        username=f"user{user_id}",
        email=f"user{user_id}@example.com",
        phone=phone,
    )
