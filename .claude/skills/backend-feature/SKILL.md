---
name: backend-feature
description: Cria ou altera funcionalidade no backend FastAPI deste repositório seguindo Ports & Adapters — domínio, caso de uso, adapter, rota, DTO e testes na ordem certa. Use ao adicionar endpoint, integração externa, persistência ou regra de negócio no backend/.
---

# Feature no backend

Leia `AGENTS.md` antes. Trabalhe de dentro para fora: o domínio não sabe que existe HTTP.

## Ordem de implementação

### 1. Domínio (`src/app/domain/`)
Modele o conceito antes do transporte. `dataclass(frozen=True, slots=True)` para entidades,
`Protocol` para a porta, exceção específica herdando de `ProviderError` quando for falha de
integração. Zero import de biblioteca externa aqui.

### 2. Caso de uso (`src/app/application/`)
Classe com dependências injetadas pelo construtor, tipadas pela porta. Um método público que
expressa a intenção (`execute`). Orquestra, não integra. Emite log estruturado do resultado
(`logger.info("evento", extra={...})`).

### 3. Adapter (`src/app/providers/`, `persistence/`, `cache/`)
Implementa a porta. Aqui entram `httpx`, `sqlalchemy`, `redis`. Traduza toda falha da biblioteca
para exceção de domínio — nada de `httpx.HTTPError` vazando para cima.

Payload externo passa por DTO Pydantic (`providers/schemas.py`) com validação real (`EmailStr`,
`StringConstraints`, validador de campo) e um `to_domain()`. Payload inválido vira
`InvalidProviderPayloadError`, não usuário corrompido.

Se o comportamento novo é uma camada sobre a resolução de usuário (cache, fallback, métrica),
implemente como **decorator** da mesma porta e plugue no container — não coloque `if` no caso de uso.

### 4. Composition root (`src/app/core/container.py`)
Único lugar que conhece implementações concretas. Recurso com ciclo de vida entra como
`@asynccontextmanager` no `AsyncExitStack`, garantindo fechamento.

### 5. API (`src/app/api/`)
- `schemas/`: DTO de request (`extra="forbid"`) e de response (`frozen=True`), com `Field`
  descrito e `json_schema_extra` de exemplo — isso alimenta o ReDoc.
- `routes/`: rota fina. Valida via schema, chama o serviço, mapeia o retorno. Sem regra de negócio.
- `error_catalog.py`: erro novo ganha `code` estável e `message` em português pronta para o
  usuário final. A mensagem é do servidor, nunca do frontend.
- `dependencies.py`: exponha o serviço como `Annotated[..., Depends(...)]`.

### 6. Testes (`tests/`)
Cubra, no mínimo: caminho feliz, falha isolada, entrada inválida rejeitada pela API. Use
`tests/factories.py`. Fakes ficam em `tests/fakes.py` e implementam a porta, sem mock de
biblioteca. Teste de endpoint sobrescreve a dependência com `app.dependency_overrides`.

### 7. Documentação
Endpoint novo aparece no README com exemplo `curl` e no `api/docs.py` com summary e description.

## Verificação

```bash
cd backend
uv run ruff check . && uv run ruff format . && uv run mypy && uv run pytest -q
```

## Armadilhas deste projeto

- Não faça retry de 404: usuário inexistente não é falha transitória.
- `asyncio.gather` nunca deve receber corrotina que propaga exceção de um item — isso cancela o
  lote inteiro. O isolamento fica dentro da corrotina.
- Toda saída para fora do processo respeita o `asyncio.Semaphore` de concorrência.
- Se adicionar campo ao `User`, atualize: DTO do provider, modelo SQLAlchemy, repositório em
  memória, schema da API, DTO e mapper do frontend, factories e README.
