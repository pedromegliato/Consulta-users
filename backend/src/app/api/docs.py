from typing import Any

TITLE = "User Fetch API"
VERSION = "1.0.0"

DESCRIPTION = """
Consulta assíncrona de múltiplos usuários em um provider HTTP externo.

**Isolamento de falha**: cada ID é resolvido de forma independente. A resposta separa
`users` (resolvidos) de `failed` (IDs que falharam por 404, timeout, erro HTTP ou
payload inválido).

**Erros**: todas as respostas de erro usam o mesmo envelope, com `code` estável,
`message` pronta para exibição ao usuário final e `request_id` para correlacionar
com os logs estruturados do servidor (também devolvido no header `X-Request-ID`).
"""

TAGS: list[dict[str, Any]] = [
    {
        "name": "users",
        "description": "Consulta de usuários em lote no provider externo.",
    },
    {
        "name": "health",
        "description": "Verificação de disponibilidade do serviço.",
    },
]

FETCH_USERS_SUMMARY = "Consulta usuários por lista de IDs"

FETCH_USERS_DESCRIPTION = """
Recebe uma lista de IDs, consulta o provider externo de forma concorrente
(limitada por `APP_MAX_CONCURRENCY`) e devolve o que foi resolvido junto dos IDs
que falharam. IDs repetidos são consultados uma única vez.

Todo usuário resolvido é gravado no espelho local, que alimenta `GET /api/users`.
"""

LIST_USERS_SUMMARY = "Lista usuários já resolvidos"

LIST_USERS_DESCRIPTION = """
Consulta o espelho local dos usuários já resolvidos. Busca, ordenação e paginação
são aplicadas no servidor: o cliente recebe apenas a página pedida, nunca a coleção
inteira.
"""
