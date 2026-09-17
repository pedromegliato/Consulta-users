from pydantic import BaseModel, ConfigDict, Field


class ErrorBody(BaseModel):
    model_config = ConfigDict(frozen=True)

    code: str = Field(description="Código estável do erro, seguro para lógica no cliente.")
    message: str = Field(description="Mensagem pronta para exibição ao usuário final.")
    details: list[str] = Field(
        default=[], description="Detalhes técnicos por campo, quando houver."
    )
    request_id: str = Field(description="Correlaciona a resposta com os logs do servidor.")


class ErrorResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        json_schema_extra={
            "examples": [
                {
                    "error": {
                        "code": "validation_error",
                        "message": "Confira os IDs informados: são aceitos apenas números "
                        "inteiros positivos.",
                        "details": ["body.user_ids: List should have at least 1 item"],
                        "request_id": "7f3c1e9a4b2d4f8a9c0e1b2d3f4a5b6c",
                    }
                }
            ]
        },
    )

    error: ErrorBody
