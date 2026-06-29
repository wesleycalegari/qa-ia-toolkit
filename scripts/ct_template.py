"""
Script de automação — [CT-ID] [Nome do CT]
Card: [PBI/BUG-XXXX] | Sprint: N | Gerado em: YYYY-MM-DD

Uso:
    python ct_template.py

Saída:
    evidencias/[CT-ID]/*.png — screenshots capturadas durante a execução
    resultado: PASS | FAIL | BLOCKED
"""

# ─────────────────────────────────────────────────
# CONFIG — ajuste antes de executar em outro ambiente
# ─────────────────────────────────────────────────
CONFIG = {
    "base_url":  "https://hml.seu-sistema.com",
    "usuario":   "usuario_hml",
    "senha":     "senha_hml",
    "massa": {
        # coloque aqui os dados descobertos dinamicamente (não fixe IDs de produção)
        "id_registro": None,   # preencher após consulta na UI ou banco
        "outro_campo": None,
    },
    "ev_dir":    "evidencias/CT-XXX-001",
}
# ─────────────────────────────────────────────────

from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

ev_dir = Path(CONFIG["ev_dir"])
ev_dir.mkdir(parents=True, exist_ok=True)

resultado = "FAIL"
mensagem_final = ""

def ev(page, nome: str, descricao: str = ""):
    """Salva screenshot de evidência."""
    caminho = ev_dir / f"{nome}.png"
    page.screenshot(path=str(caminho))
    print(f"  📸 {nome}.png — {descricao}")
    return caminho

def extrair_mensagem(page) -> str:
    """Tenta extrair mensagem de sucesso ou erro da tela."""
    return page.evaluate("""() => {
        const sel = '.alert, .mensagem, .validation-summary, #lblMensagem, [role=alert]';
        const el = document.querySelector(sel);
        return el ? el.innerText.trim() : '';
    }""") or ""

def login(page):
    page.goto(CONFIG["base_url"] + "/login")
    page.fill("[name=usuario], #usuario, input[type=text]", CONFIG["usuario"])
    page.fill("[name=senha], #senha, input[type=password]", CONFIG["senha"])
    page.click("button[type=submit], input[type=submit], .btn-login")
    page.wait_for_load_state("networkidle")

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False)
    ctx = browser.new_context(viewport={"width": 1280, "height": 720})
    page = ctx.new_page()

    try:
        # ── LOGIN ──────────────────────────────────────
        print("→ Login")
        login(page)
        ev(page, "01_login_ok", "Tela inicial após login")

        # ── NAVEGAÇÃO ──────────────────────────────────
        # TODO: substituir pelos cliques reais do módulo
        print("→ Navegar até o módulo")
        page.click("text=[MENU PRINCIPAL]")
        page.click("text=[SUBMENU]")
        page.wait_for_load_state("networkidle")
        ev(page, "02_tela_modulo", "Tela do módulo aberta")

        # ── AÇÃO PRINCIPAL ─────────────────────────────
        # TODO: preencher campos e executar a ação
        print("→ Executar ação principal")
        page.fill("#campo1", "valor1")
        page.fill("#campo2", "valor2")
        ev(page, "03_formulario_preenchido", "Formulário com dados preenchidos")

        page.click("text=Salvar")
        page.wait_for_load_state("networkidle")

        # ── VERIFICAÇÃO ────────────────────────────────
        mensagem = extrair_mensagem(page)
        ev(page, "04_resultado", f"Resultado: {mensagem}")

        # TODO: ajustar a condição de sucesso para este CT
        if "sucesso" in mensagem.lower() or "gravado" in mensagem.lower():
            resultado = "PASS"
        else:
            resultado = "FAIL"
            mensagem_final = f"Mensagem inesperada: '{mensagem}'"

    except PWTimeout as e:
        resultado = "BLOCKED"
        mensagem_final = f"Timeout: {e}"
        try:
            ev(page, "99_erro", "Estado no momento do erro")
        except Exception:
            pass

    except Exception as e:
        resultado = "FAIL"
        mensagem_final = str(e)
        try:
            ev(page, "99_erro", "Estado no momento do erro")
        except Exception:
            pass

    finally:
        browser.close()

# ── RESULTADO FINAL ────────────────────────────────
print()
print(f"{'='*50}")
print(f"  RESULTADO: {resultado}")
if mensagem_final:
    print(f"  Detalhe:  {mensagem_final}")
print(f"  Evidências em: {ev_dir}")
print(f"{'='*50}")
