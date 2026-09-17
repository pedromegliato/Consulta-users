# CLAUDE.md

As regras deste repositório estão em **[AGENTS.md](./AGENTS.md)** — leia antes de qualquer
alteração. Este arquivo cobre apenas o que é específico do Claude Code.

## Skills disponíveis

| Skill | Quando usar |
| --- | --- |
| `/code-review` | Revisar um diff antes de commit ou PR. |
| `/backend-feature` | Criar ou alterar caso de uso, adapter ou endpoint no `backend/`. |
| `/frontend-feature` | Criar ou alterar componente, hook ou tela no `frontend/`. |

## Fluxo esperado

1. Leia o código existente da camada antes de escrever. Este projeto tem padrões definidos
   (portas, decorators, DTO/domínio, união discriminada de estado) — siga-os em vez de
   introduzir um novo.
2. Faça a menor mudança que resolve o pedido. Não refatore o que não foi pedido.
3. Rode os comandos de verificação do AGENTS.md e só então reporte conclusão.
4. Ao reportar, diga o que ficou de fora e por quê.

## Hooks de git

`pre-commit` roda `lint-staged` (formata e corrige o que foi alterado) e `pre-push` roda lint,
tipagem e testes dos dois apps. Não use `--no-verify`.

## Limites

- Não adicione dependência sem necessidade clara; justifique no PR.
- Não crie camada, pasta ou abstração "para o futuro".
- Não escreva comentário explicando o óbvio.
- Não altere o contrato da API sem atualizar DTO do frontend, testes e README.
