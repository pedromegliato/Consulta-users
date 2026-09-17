---
name: frontend-feature
description: Cria ou altera funcionalidade no frontend React + TypeScript deste repositório — primitivo de UI com variantes, feature, hook, DTO e mapper, mobile-first e com erro amigável. Use ao adicionar tela, componente, hook ou chamada de API no frontend/.
---

# Feature no frontend

Leia `AGENTS.md` antes. Regra de ouro: primitivo de UI não conhece regra de negócio, e
componente não busca dado — quem busca é o hook.

## Onde cada coisa vai

| Pasta | Conteúdo | Pode importar |
| --- | --- | --- |
| `ui/` | Primitivo reutilizável com variantes | nada do projeto além de `ui/` |
| `features/` | Composição para um caso de uso | `ui/`, `domain/`, `lib/`, `hooks/` |
| `hooks/` | Estado e efeitos | `api/`, `domain/`, `lib/` |
| `api/` | Client HTTP, DTO do fio, mappers | `domain/` |
| `domain/` | Modelo da aplicação | nada |
| `lib/` | Funções puras | `api/` só para tipos |

## Ordem de implementação

### 1. Contrato (`api/dto.ts`, `domain/`)
DTO espelha o fio (`snake_case`, exatamente como o backend responde). O modelo de domínio é
`camelCase` e independente. A conversão vive em `api/mappers.ts` — nunca no componente.

### 2. Client (`api/usersClient.ts`)
Toda função recebe `AbortSignal` opcional. Resposta não-ok vira `ApiError` com `code`, `status`,
`serverMessage`, `details` e `requestId`. Retorne domínio, não DTO.

### 3. Hook (`hooks/`)
Estado como união discriminada:

```ts
type State =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; result: T }
  | { status: 'error'; error: UserFacingError };
```

Nada de `isLoading` + `data` + `error` soltos. Cancele a requisição anterior com
`AbortController` e limpe no unmount. Ignore o erro quando `signal.aborted`.

### 4. Primitivo (`ui/`)
Só crie se for reutilizável. Variantes por prop tipada como união literal, traduzidas em classe
BEM (`btn btn--primary btn--sm`), nunca estilo inline. Componha com `cx()`. Estenda os atributos
nativos (`ButtonHTMLAttributes`, `InputHTMLAttributes`) e repasse o resto com `...rest`.

Acessibilidade não é opcional: `label` associado por `id`, `aria-sort` em coluna ordenável,
`aria-live` em região que muda sozinha, `role="alert"` em erro.

### 5. Feature (`features/`)
Compõe primitivos e recebe o controller/dados por props. Colunas de tabela ficam em constante no
topo do arquivo, com `sortField` para o que o servidor sabe ordenar.

### 6. Erro amigável (`lib/errorMessages.ts`)
A mensagem vem do backend (`serverMessage`). O mapa local só cobre o que o servidor não consegue
responder: falha de rede e resposta sem envelope. Não duplique o catálogo do backend.
Exiba o `requestId` como código de referência e detalhe técnico dentro de `<details>`.

### 7. Estilo (`styles.css`)
**Mobile-first**: estilo base atende telas pequenas; `@media (min-width: 640px)` promove.
Cores por variável CSS em `:root`. Alvo de toque de 44px, `font-size: 1rem` em input.
Se esconder algo no mobile (cabeçalho de tabela, por exemplo), ofereça o equivalente acessível —
foi assim que nasceu o `.sort-controls`.

### 8. Testes (`*.test.ts`)
Teste função pura (parser, formatador, mapper, tradução de erro) e contrato do client com
`vi.stubGlobal('fetch', ...)`. Use `src/test/factories.ts`.

## Verificação

```bash
cd frontend && npm run typecheck && npm test
```

Valide no browser em 390px e em 1280px antes de dar por pronto.

## Armadilhas deste projeto

- Paginação, busca e ordenação são **server-side**. Não filtre nem ordene array no cliente.
- `exactOptionalPropertyTypes` está ligado: `signal?: AbortSignal` não pode ir direto para
  `RequestInit` — passe `signal ?? null`.
- Formatação depende de locale: não aplique máscara brasileira em dado que pode ser estrangeiro
  sem validar o padrão antes.
