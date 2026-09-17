# AGENTS.md

Instruções para qualquer agente de código que trabalhe neste repositório.

## O que é este projeto

Monorepo com `backend/` (FastAPI, Ports & Adapters) e `frontend/` (React + TypeScript).
Consulta múltiplos usuários em um provider HTTP externo de forma assíncrona, isolando falhas.

## Comandos

```bash
# backend
cd backend && uv sync
uv run uvicorn app.main:app --reload
uv run ruff check . && uv run ruff format . && uv run mypy && uv run pytest

# frontend
cd frontend && npm install
npm run dev
npm run typecheck && npm test

# tudo
docker compose up --build
```

Nenhuma mudança é considerada pronta sem `ruff check`, `mypy`, `pytest`, `tsc --noEmit` e
`vitest` passando.

## Princípios obrigatórios

**SRP** — uma unidade, uma razão para mudar. Serviço orquestra, adapter integra, rota traduz
HTTP. Se um arquivo precisa de "e" para ser descrito, ele tem responsabilidades demais.

**DI** — dependências entram pelo construtor, tipadas pela porta (`Protocol`), nunca instanciadas
dentro de quem as usa. O único lugar que conhece implementações concretas é o composition root
(`backend/src/app/core/container.py`). `Depends` do FastAPI só na borda HTTP.

**OCP** — comportamento novo entra como novo adapter ou decorator implementando a porta
existente, não como `if` dentro do caso de uso.

**DIP** — `domain/` e `application/` não importam `httpx`, `sqlalchemy`, `redis` ou `fastapi`.
Essa regra é verificável: se um import desses aparecer nessas pastas, a mudança está errada.

**DRY** — uma regra vive em um lugar. O catálogo de mensagens de erro é do backend; o frontend
consome, não replica. Mapeamento de DTO para domínio fica no mapper, não espalhado.

**KISS** — resolva o problema pedido. Abstração especulativa, camada "para o futuro" e
configuração que ninguém usa são dívida, não design.

**YAGNI** — não escreva validador, campo ou endpoint que nada consome.

## Regras de código

**Comentários são proibidos**, salvo quando explicam um *porquê* que o código não expressa
(decisão de negócio, workaround com link). Comentário que descreve o que a linha faz é ruído:
extraia um método com nome melhor.

**Nada de defensividade falsa.** Não engula exceção sem tratar, não retorne `None` "por
segurança", não valide o que o tipo já garante. Exceção inesperada deve subir. A única captura
ampla do projeto é a fronteira de isolamento por usuário, e ela é deliberada.

**Tipagem completa.** `mypy --strict` no backend e `strict` + `exactOptionalPropertyTypes` +
`noUncheckedIndexedAccess` no frontend. Sem `Any` sem motivo, sem `as` para calar o compilador,
sem `# type: ignore` sem comentário justificando.

**Contratos explícitos.** DTO de fronteira é separado do modelo de domínio, nos dois lados:
`api/schemas/` e `providers/schemas.py` no backend, `api/dto.ts` e `domain/` no frontend, com
mappers entre eles. Payload externo é validado antes de virar domínio.

**Nomes em português no texto de usuário, código em inglês.** Identificadores, arquivos e
mensagens de log em inglês; mensagens exibidas ao usuário e documentação em português.

## Arquitetura do backend

```
domain/        modelos, exceções, portas (Protocol), paginação/query. Zero dependência externa.
application/   casos de uso. Orquestram portas, não conhecem HTTP nem SQL.
providers/     adapters do provider externo (httpx, retry, DTO de fronteira).
persistence/   espelho: repositório PostgreSQL e em memória.
cache/         cache de usuário: Redis e memória.
api/           rotas, schemas, catálogo de erros, middleware, DI.
core/          config, logging estruturado, composition root.
```

A cadeia `CachedUserProvider → MirroringUserProvider → HttpUserProvider` é composta no container.
Comportamento novo na resolução de usuário entra como novo elo, não como `if`.

## Arquitetura do frontend

```
ui/            primitivos reutilizáveis com variantes. Não conhecem regra de negócio.
features/      composição de primitivos para um caso de uso.
hooks/         estado e efeitos. Toda requisição é cancelável por AbortController.
api/           client HTTP, DTOs do fio e mappers.
domain/        modelo da aplicação.
lib/           funções puras (parse, formatação, tradução de erro).
```

Estado assíncrono é união discriminada (`idle | loading | success | error`), nunca booleanos
soltos. Componente de UI recebe dados por props; quem busca é o hook.

Layout é **mobile-first**: o estilo base atende telas pequenas e `@media (min-width: 640px)`
promove. Alvo de toque mínimo de 44px, input com 16px.

## Erros e observabilidade

O backend é dono do contrato de erro: `code` estável, `message` pronta para o usuário final e
`request_id`. O frontend só traduz o que o servidor não pode saber (falha de rede).

Todo log é JSON estruturado com `request_id` propagado por `contextvars`. Log novo usa
`logger.info("evento_em_snake_case", extra={...})`, nunca string interpolada.

## Testes

Teste comportamento observável pela porta pública, não implementação. Use as factories
(`backend/tests/factories.py`, `frontend/src/test/factories.ts`) em vez de montar objetos à mão.
Nome de teste descreve o comportamento: `test_failure_of_one_user_does_not_stop_the_others`.

Toda correção de bug começa por um teste que falha.

## Antes de entregar

1. Rode lint, tipagem e testes dos dois lados.
2. Releia o diff procurando comentário supérfluo, `Any`, duplicação e abstração não usada.
3. Se criou um arquivo novo, confirme que ele tem uma única responsabilidade.
