---
name: code-review
description: Revisa o diff atual deste repositório contra os princípios do AGENTS.md (SRP, DI, DIP, DRY, KISS), caça AI smell, defensividade falsa, tipagem frouxa e quebra de contrato. Use antes de commit ou de abrir PR, ou quando pedirem revisão de código.
---

# Revisão de código

## Passo 1 — obter o diff

```bash
git diff HEAD          # mudanças não commitadas
git diff main...HEAD   # branch inteira
```

Leia também os arquivos vizinhos aos alterados: metade dos problemas é duplicação de algo que já
existe uma pasta acima.

## Passo 2 — checklist

Revise nesta ordem e pare em cada item com evidência concreta (arquivo e linha).

### Corretude
- Exceção capturada ampla demais, engolindo erro que deveria subir.
- `zip`, fatiamento ou índice sem garantia de tamanho.
- `async` sem `await`, requisição sem cancelamento, efeito sem cleanup.
- Contrato do backend divergente do DTO do frontend.

### SRP e coesão
- Arquivo que só se descreve com "e": tem responsabilidade demais.
- Caso de uso que conhece `httpx`, `sqlalchemy`, `redis` ou `fastapi`. Proibido.
- Componente de UI que busca dados por conta própria em vez de receber por props.

### DI e OCP
- Dependência instanciada dentro de quem a usa em vez de injetada pela porta.
- `if` sobre tipo de provider/adapter onde caberia um novo elo na cadeia de decorators.
- Implementação concreta importada fora do `core/container.py`.

### DRY
- Regra replicada nos dois lados (mensagem de erro, validação, formatação).
- Mapeamento DTO → domínio espalhado em vez de centralizado no mapper.
- Constante mágica repetida.

### KISS e YAGNI
- Abstração com um único uso e nenhum segundo previsto.
- Parâmetro de configuração que ninguém lê.
- Camada criada "para o futuro".

### AI smell
- Comentário que narra o que a linha faz (`# incrementa o contador`).
- Docstring que repete o nome da função.
- `try/except` que só faz `pass` ou `log` e segue como se nada tivesse acontecido.
- Validação redundante do que o tipo já garante.
- Nome genérico: `data`, `result`, `handle`, `process`, `manager`, `helper`.
- Código morto deixado "por precaução".

### Tipagem e contratos
- `Any`, `as`, `# type: ignore` sem justificativa.
- Optional que deveria ser união discriminada.
- DTO de fronteira sem validação do payload externo.
- Campo novo na API sem atualizar DTO, mapper, testes e README.

### Testes
- Mudança de comportamento sem teste.
- Teste que verifica implementação (chamadas internas) em vez de comportamento.
- Objeto montado à mão onde existe factory.

### Segurança e observabilidade
- Dado sensível em log ou em mensagem de erro exposta ao usuário.
- Erro novo sem `code` no catálogo do backend.
- Operação relevante sem log estruturado correlacionável por `request_id`.

## Passo 3 — verificar

```bash
cd backend  && uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest -q
cd frontend && npm run typecheck && npm test
```

## Passo 4 — reportar

Ordene por severidade. Para cada achado: arquivo e linha, o problema em uma frase, o cenário
concreto em que dá errado e a correção sugerida. Não relate estilo que o ruff/tsc já cobre.
Se nada relevante apareceu, diga isso — não invente achado para preencher a lista.
