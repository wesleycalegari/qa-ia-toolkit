# Catálogo de Scripts de Automação

> **Regra:** consultar este arquivo ANTES de criar qualquer novo script.
> Se o módulo/seguradora/cenário já tiver script aprovado, reusar em vez de criar novo.
> Atualizar ao final de cada sprint com os scripts gerados/promovidos.

---

## Como usar

```
Para cada CT a ser executado:
  1. Pesquisar neste arquivo pelo módulo, seguradora ou PBI
  2. SE encontrado e APROVADO: usar o script (passo 0c do validacao-testes)
  3. SE não encontrado: executar via MCP e criar script após CT aprovado
```

---

## Regressivo (_regressivo/)

> Scripts promovidos — executados em todo novo release

| Script | Módulo | Seguradora | Sprints PASS | Observação |
|--------|--------|------------|-------------|------------|
| | | | | |

---

## Sprint Atual

> Scripts criados nesta sprint — candidatos ao regressivo

| Script | Módulo | Card | CT(s) | Status | Reusar quando |
|--------|--------|------|-------|--------|---------------|
| | | | | | |

---

## Sprints Anteriores

> Scripts validados em sprints passadas ainda não promovidos

| Script | Sprint | Módulo | Card | Observação |
|--------|--------|--------|------|------------|
| | | | | |

---

## Template de entrada

```markdown
### ct_[modulo]_[cenario].py
- **Cobre:** [Módulo] > [Tela] > [Ação específica]
- **Card:** [PBI/BUG-XXXX]
- **CTs:** [CT-XXX-001, CT-XXX-002]
- **Sprints PASS:** [Sprint N, Sprint N+1]
- **Status:** Candidato / Promovido ao regressivo
- **Reusar quando:** [Qualquer reteste de X, qualquer CT de Y com mesmo fluxo]
```
