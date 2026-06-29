# Configuração Global — [Nome do QA]

## Auto-aplicação de skills por contexto

### QA — Planejamento de Testes
**Quando ativar:** usuário pede para criar plano de teste, analisar card para QA, gerar casos de teste,
montar plano, revisar critérios de aceite, ou qualquer atividade de planejamento.

**Ação:** ler e aplicar o arquivo:
`~/.claude/commands/qa-expert.md`

### QA — Execução e Validação
**Quando ativar:** usuário pede para executar testes, validar CT, capturar evidências,
atualizar plano com resultados, marcar CT como aprovado/reprovado, rodar via Playwright.

**Ação:** ler e aplicar o arquivo:
`~/.claude/commands/validacao-testes.md`

---

## Regras globais sempre ativas

- **Playwright MCP sempre** — qualquer interação com browser usa o MCP, nunca scripts locais
- **Navegar por clique** — sempre partir do login e clicar pelo menu; nunca URL direta
- **Evidências obrigatórias** — toda ação em sistema web com resultado relevante gera screenshot
- **Nunca publicar sem revisão** — apresentar sempre ao responsável antes de qualquer push/publicação no AzDO

## Regra crítica — ler a skill antes de agir

**Antes de qualquer ação QA, OBRIGATÓRIO:**
1. Ler o arquivo da skill correspondente
2. Verificar item a item contra o checklist do arquivo
3. Para criar qualquer Work Item filho no AzDO: consultar o pai via API antes de criar,
   copiar `AreaPath` e `IterationPath` exatos — nunca usar o projeto raiz
