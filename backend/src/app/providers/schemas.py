from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints, field_validator

from app.domain.user import User
from app.providers.phone import normalize_phone

RequiredText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class ProviderUserPayload(BaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)

    id: Annotated[int, Field(gt=0)]
    name: RequiredText
    username: RequiredText
    email: EmailStr
    phone: str | None = None

    @field_validator("phone")
    @classmethod
    def _normalize_phone(cls, value: str | None) -> str | None:
        return normalize_phone(value)

    def to_domain(self) -> User:
        return User(
            id=self.id,
            name=self.name,
            username=self.username,
            email=str(self.email),
            phone=self.phone,
        )
