from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    status: str


@router.get("/health", response_model=HealthResponse, summary="Verifica se o serviço responde")
async def health() -> HealthResponse:
    return HealthResponse(status="ok")
