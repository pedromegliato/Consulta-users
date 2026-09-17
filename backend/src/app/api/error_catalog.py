from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ErrorDefinition:
    code: str
    status_code: int
    message: str


VALIDATION_ERROR = ErrorDefinition(
    code="validation_error",
    status_code=422,
    message="Confira os IDs informados: são aceitos apenas números inteiros positivos.",
)

INTERNAL_ERROR = ErrorDefinition(
    code="internal_error",
    status_code=500,
    message="Não conseguimos concluir a consulta agora. Tente novamente em instantes.",
)

_BY_STATUS = {
    400: ErrorDefinition(
        code="bad_request",
        status_code=400,
        message="A requisição enviada não pôde ser processada. Revise os dados e tente de novo.",
    ),
    404: ErrorDefinition(
        code="not_found",
        status_code=404,
        message="O recurso solicitado não existe neste servidor.",
    ),
    405: ErrorDefinition(
        code="method_not_allowed",
        status_code=405,
        message="Esta operação não é permitida neste endereço.",
    ),
    429: ErrorDefinition(
        code="too_many_requests",
        status_code=429,
        message="Muitas consultas em pouco tempo. Aguarde alguns segundos e tente de novo.",
    ),
    503: ErrorDefinition(
        code="service_unavailable",
        status_code=503,
        message="O serviço está temporariamente indisponível. Tente novamente em instantes.",
    ),
}


def definition_for_status(status_code: int) -> ErrorDefinition:
    known = _BY_STATUS.get(status_code)
    if known is not None:
        return known
    if status_code >= 500:
        return INTERNAL_ERROR
    return ErrorDefinition(
        code="request_error",
        status_code=status_code,
        message="Não foi possível concluir a requisição. Revise os dados e tente de novo.",
    )
