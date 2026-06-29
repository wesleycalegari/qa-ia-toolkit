# Skill de domínio — [NOME DO SISTEMA]

> **Como usar este template:**
> Preencha cada seção com as informações do seu sistema.
> Salve como `~/.claude/commands/[meu-sistema]-expert.md`.
> Quanto mais completo, melhores serão os CTs gerados.
>
> **Dica:** se o projeto tiver código-fonte, manuais ou documentação acessíveis,
> adicione a instrução de leitura na seção "Fontes de verdade" abaixo e
> deixe o Claude aprender diretamente dos arquivos — você não precisa documentar tudo aqui.

---

## Sistema

- **Nome:** [Ex: Portal de Vendas / ERP / API de Pagamentos]
- **Tipo:** [Web / Mobile / API / Desktop]
- **Stack:** [Ex: React + Node.js / .NET + SQL Server / Laravel]
- **Descrição:** [Uma frase descrevendo o que o sistema faz]

---

## Ambientes

| Ambiente | URL | Observação |
|----------|-----|------------|
| HML | https://hml.[sistema].com | Usar para todos os testes |
| STG | https://stg.[sistema].com | Somente pré-release |

**Credenciais:** ver `.env` do projeto (`USUARIO_HML`, `SENHA_HML`)

---

## Fontes de verdade

> Instrua o Claude a ler estes arquivos antes de gerar qualquer CT.
> Remove a necessidade de documentar tudo manualmente nesta skill.

```
# Antes de gerar qualquer CT, ler:
- Manuais:  [caminho]/manuais/          ← fluxos e regras de negócio
- Features: [caminho]/features/         ← comportamentos verificados in loco
- Código:   [caminho]/src/              ← regras nos services/validators
- Swagger:  [caminho]/docs/api/         ← contratos de API
- BDD:      [caminho]/features/*.feature ← cenários Gherkin (se existir)
```

---

## Módulos principais

> Liste os módulos que o QA precisará testar. Para cada um, descreva o fluxo típico.

### [Módulo 1 — Ex: Cadastro de Clientes]
- **Acesso:** Menu > Clientes > Novo
- **Fluxo:** Preencher nome, CPF/CNPJ, e-mail → Salvar → Confirmar na lista
- **Campos obrigatórios:** Nome, CPF/CNPJ, E-mail
- **Validações importantes:** CPF deve ser válido; e-mail deve ter formato correto

### [Módulo 2 — Ex: Pedidos]
- **Acesso:** Menu > Vendas > Pedidos > Novo Pedido
- **Fluxo:** Selecionar cliente → Adicionar itens → Confirmar → Aprovação
- **Estados:** Rascunho → Aprovação Pendente → Aprovado → Faturado → Entregue

### [Módulo N — ...]
- ...

---

## Regras de negócio críticas para QA

> Liste as regras que MAIS impactam os testes — limites, bloqueios, cálculos, permissões.

- **[Regra 1]:** [Ex: Pedido só pode ser aprovado se cliente tiver limite de crédito disponível]
- **[Regra 2]:** [Ex: Data de entrega não pode ser anterior à data de hoje]
- **[Regra 3]:** [Ex: Desconto máximo sem aprovação gerencial é 10%]
- **[Regra N]:** ...

---

## Perfis de usuário relevantes para testes

| Perfil | O que pode fazer | O que NÃO pode |
|--------|-----------------|----------------|
| Operador | Criar e editar pedidos | Aprovar, excluir |
| Gerente | Tudo do Operador + Aprovar | Excluir clientes |
| Admin | Tudo | — |

---

## Convenção de IDs dos Casos de Teste

```
CT-[MÓDULO]-[NNN]

Módulos:
  CAD = Cadastro          (clientes, fornecedores, produtos)
  PED = Pedidos           (criação, edição, aprovação)
  FAT = Faturamento       (emissão de nota, pagamento)
  REL = Relatórios        (exportação, filtros)
  ADM = Administração     (usuários, permissões, configurações)
  API = Testes de API     (contratos, erros, autenticação)
  REG = Regressão         (CTs de regressão cross-módulo)

Exemplos:
  CT-CAD-001  CT-PED-015  CT-FAT-003  CT-API-007
```

---

## Massa de dados — como obter

> Instrua o Claude sobre como conseguir dados para os testes.

```
1. Consultar o banco HML diretamente (preferencial):
   → Servidor: [servidor]
   → Banco: [banco-hml]
   → Usuário: ver .env (DB_USER, DB_PASS)
   
   Queries úteis:
   → Clientes ativos:  SELECT TOP 5 id, nome, cpf FROM clientes WHERE ativo=1
   → Pedidos abertos:  SELECT TOP 5 id FROM pedidos WHERE status='pendente'

2. Criar via UI do sistema (quando não existe massa):
   → Usar Playwright MCP para cadastrar o registro necessário
   → Anotar o ID gerado e fixar no plano

3. Nunca usar dados de produção
```

---

## Board e sprint do Azure DevOps

- **Organização:** [SuaOrganizacao]
- **Projeto:** [SeuProjeto]
- **Board:** [Nome do Board]
- **Sprint atual:** [Sprint N]
- **Filtro de cards:** `[System.IterationPath] = '[SeuProjeto]\Sprint_N'`

---

## Navegação padrão

> Informe como navegar até cada módulo principal (importante para o Playwright MCP).

```
Login:
  URL: https://hml.[sistema].com/login
  Campo usuário: [seletor do campo]
  Campo senha:   [seletor do campo]
  Botão:         [seletor do botão]

[Módulo 1]:
  1. Clicar em [Item de menu principal]
  2. Clicar em [Submenu]
  3. Clicar em [Ação]

[Módulo 2]:
  1. ...
```

---

## Mensagens padrão do sistema

> Liste as mensagens de sucesso e erro mais comuns para os CTs saberem o que verificar.

| Situação | Mensagem exata |
|----------|----------------|
| Registro salvo | "[Texto exato que aparece na tela]" |
| Validação de campo obrigatório | "[Texto exato]" |
| Sem permissão | "[Texto exato]" |
| Erro de servidor | "[Texto exato]" |

---

## Observações específicas do sistema

> Comportamentos não óbvios que o QA precisa conhecer.

- **[Observação 1]:** [Ex: Após salvar um pedido, o sistema redireciona automaticamente para a lista — não há mensagem de sucesso em tela]
- **[Observação 2]:** [Ex: O campo de CPF aplica máscara automática — testar sempre com e sem pontuação]
- **[Observação N]:** ...
