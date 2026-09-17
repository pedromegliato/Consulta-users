import pytest
from pydantic import ValidationError

from app.providers.phone import normalize_phone
from app.providers.schemas import ProviderUserPayload

VALID_PAYLOAD = {
    "id": 1,
    "name": "Leanne Graham",
    "username": "Bret",
    "email": "leanne@example.com",
    "phone": "1-770-736-8031 x56442",
    "website": "hildegard.org",
}


def test_maps_payload_ignoring_unknown_fields() -> None:
    user = ProviderUserPayload.model_validate(VALID_PAYLOAD).to_domain()

    assert user.id == 1
    assert user.email == "leanne@example.com"
    assert user.phone == "17707368031"


@pytest.mark.parametrize(
    "field, value",
    [
        ("email", "nao-e-um-email"),
        ("name", "   "),
        ("id", 0),
    ],
)
def test_rejects_invalid_field(field: str, value: object) -> None:
    with pytest.raises(ValidationError):
        ProviderUserPayload.model_validate({**VALID_PAYLOAD, field: value})


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("(11) 98765-4321", "11987654321"),
        ("1-770-736-8031 x56442", "17707368031"),
        ("ramal 4321", None),
        ("123", None),
        (None, None),
    ],
)
def test_normalizes_phone(raw: str | None, expected: str | None) -> None:
    assert normalize_phone(raw) == expected
