from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class User:
    id: int
    name: str
    username: str
    email: str
    phone: str | None = None
