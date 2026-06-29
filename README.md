# QA × IA Toolkit

Metodologia e ferramentas para integrar o **Claude Code** ao ciclo de qualidade de software.
Desenvolvido e validado ao longo de 9 sprints no projeto CITWEB/CITNET (NStech).

---

## O que é este toolkit

Um conjunto de **skills, templates e scripts** que permitem ao Claude Code atuar como par de QA —
lendo cards do Azure DevOps, navegando na aplicação via Playwright MCP, escrevendo casos de teste,
executando e gerando todos os artefatos de evidência.

**O que o Claude faz:**
- Lê e interpreta cards do Azure DevOps
- Navega na aplicação real via Playwright MCP
- Escreve casos de teste com passos precisos e verificados
- Gera planos HTML interativos com dashboard de execução
- Executa testes e captura evidências por CT
- Publica resultados no GitHub Pages e notifica o time no Teams

**O que ele nunca faz sozinho:**
- Não publica sem aprovação do responsável
- Não cria bugs no AzDO sem confirmação humana
- Não inventa dados — confirma antes de assumir

---

## Conteúdo do repositório

```
qa-ia-toolkit/
  skills/
    qa-expert.md           ← skill de planejamento de testes (universal)
    validacao-testes.md    ← skill de execução e evidências (universal)
    dominio-template.md    ← template para skill do seu sistema
  templates/
    CLAUDE.md              ← configuração global do Claude Code
    CLAUDE-projeto.md      ← configuração por projeto
    .mcp.json              ← Playwright MCP config
    .env.example           ← variáveis de credenciais
    _catalogo_scripts.md   ← índice de scripts de automação
  scripts/
    publicar.py            ← publica plano de teste no GitHub Pages
    rodar_regressivo.py    ← executa suite de regressão e gera dashboard
    ct_template.py         ← template de script Python por CT
  plano-template/
    index.html             ← template HTML do plano de teste (dark theme)
    evidencias/            ← estrutura de pastas por CT
  docs/
    apresentacao.html      ← apresentação completa do fluxo de trabalho
```

---

## Início rápido (5 passos)

### 1. Instale o Claude Code
```bash
npm install -g @anthropic-ai/claude-code
```

### 2. Copie as skills globais
```bash
# Windows
copy skills\qa-expert.md      %USERPROFILE%\.claude\commands\qa-expert.md
copy skills\validacao-testes.md %USERPROFILE%\.claude\commands\validacao-testes.md
copy skills\dominio-template.md %USERPROFILE%\.claude\commands\meu-sistema-expert.md
```

### 3. Configure o Playwright MCP
Copie `templates/.mcp.json` para a raiz do seu projeto e instale:
```bash
npm install -g @playwright/mcp
```

### 4. Crie as credenciais
Copie `templates/.env.example` para `.env` e preencha com seu PAT do Azure DevOps.

### 5. Adapte a skill de domínio
Edite `~/.claude/commands/meu-sistema-expert.md` com as informações do seu sistema:
telas, módulos, regras de negócio, convenção de IDs dos CTs.

> **Dica:** se o projeto tiver código-fonte ou manuais disponíveis, instrua o Claude a lê-los
> diretamente — ele aprende as regras sem que o QA precise documentar tudo manualmente.

---

## Fluxo de trabalho

```
Card AzDO                   → Ler PBI + tasks
    ↓
Gate 1                      → Card completo? Se não: comentar com dúvidas
    ↓
Playwright MCP              → Mapear tela real (snapshot + executar fluxo)
    ↓
Rascunho de CTs             → Formato CT-XXX-NNN, passos verificados
    ↓
Gate 2                      → Revisão individual de cada CT
    ↓
Excel + HTML                → Gravar passos + gerar plano dark theme
    ↓
Gate 3                      → Revisão do plano completo
    ↓
GitHub Pages                → Publicar plano
    ↓
AzDO Comment                → Link + @validador solicitando validação
    ↓
Gate 4                      → Aguardar validação + PBI liberado para homologação
    ↓
Execução                    → Playwright MCP por CT + evidências
    ↓
CT Reprovado?               → Bug report HTML → Gate confirmação → AzDO task
    ↓
Resultado final             → Comentário HTML rico no AzDO + Teams webhook
```

---

## Princípios que funcionam em qualquer projeto

| Princípio | Regra |
|-----------|-------|
| Navegação | Sempre por clique — nunca URL direta |
| Evidência | Screenshot em toda ação relevante |
| Mensagem de erro | Ler o texto exato antes de classificar o CT |
| Gates | Nunca publicar no AzDO sem aprovação explícita |
| Mapeamento | Ver a tela real antes de escrever qualquer CT |
| Estado | Estado limpo antes de cada CT |
| Dados | Nunca deduzir — confirmar antes de prosseguir |
| Bug | Confirmação humana antes de abrir card no AzDO |

---

## Sobre o projeto de origem

Este toolkit foi desenvolvido no projeto **CITWEB/CITNET** (sistemas de seguro de transporte — NStech)
ao longo das Sprints 4 a 9 de 2026, cobrindo 30+ cards, 500+ casos de teste e 241 CTs automatizados.

---

## Licença

MIT — use, adapte e compartilhe.
