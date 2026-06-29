"""
rodar_regressivo.py — executa toda a suite de regressão e gera dashboard HTML

Uso:
    python rodar_regressivo.py
    python rodar_regressivo.py --modulo cadastro   # apenas um módulo
    python rodar_regressivo.py --dry-run           # lista scripts sem executar

Saída:
    evidencias/regressivo_YYYY-MM-DD_HH-MM/
        dashboard.html   ← resultados com filtros e galeria de screenshots
        [modulo]/        ← evidências por módulo
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

REGRESSIVO_DIR = Path("testes-automatizados/_regressivo")
EV_BASE = Path("evidencias")

def listar_scripts(modulo: str = None) -> list[Path]:
    scripts = sorted(REGRESSIVO_DIR.glob("*.py"))
    if modulo:
        scripts = [s for s in scripts if modulo in s.name]
    return scripts

def rodar_script(script: Path, ev_dir: Path) -> dict:
    env = os.environ.copy()
    env["EV_DIR"] = str(ev_dir / script.stem)
    inicio = datetime.now()

    resultado = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True, text=True, env=env, timeout=300
    )

    duracao = (datetime.now() - inicio).total_seconds()
    status = "PASS" if resultado.returncode == 0 else "FAIL"

    # Detectar BLOCKED na saída
    saida = resultado.stdout + resultado.stderr
    if "BLOCKED" in saida.upper():
        status = "BLOCKED"

    return {
        "script": script.name,
        "status": status,
        "duracao": round(duracao, 1),
        "saida": saida[-2000:],  # últimas 2000 chars
        "evidencias": str(env["EV_DIR"]),
    }

def gerar_dashboard(resultados: list[dict], ev_dir: Path):
    total = len(resultados)
    passou = sum(1 for r in resultados if r["status"] == "PASS")
    falhou = sum(1 for r in resultados if r["status"] == "FAIL")
    bloq   = sum(1 for r in resultados if r["status"] == "BLOCKED")
    pct = round(passou / total * 100) if total else 0

    linhas_cts = ""
    for r in resultados:
        cor = {"PASS": "#22d3a0", "FAIL": "#f43f5e", "BLOCKED": "#fbbf24"}.get(r["status"], "#888")
        linhas_cts += f"""
        <tr>
          <td style="font-family:monospace;font-size:.8rem">{r['script']}</td>
          <td style="color:{cor};font-weight:700;text-align:center">{r['status']}</td>
          <td style="text-align:center;color:#888">{r['duracao']}s</td>
        </tr>"""

    html = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>Regressivo — {datetime.now():%d/%m/%Y %H:%M}</title>
<style>
  * {{ box-sizing:border-box; margin:0; padding:0 }}
  body {{ background:#060c1a; color:#c4d3e6; font-family:'Segoe UI',system-ui,sans-serif; padding:32px }}
  h1 {{ color:#eef2f8; font-size:1.6rem; margin-bottom:8px }}
  .sub {{ color:#4a6280; font-size:.85rem; margin-bottom:32px }}
  .metrics {{ display:flex; gap:16px; margin-bottom:32px; flex-wrap:wrap }}
  .m {{ background:#0e1829; border:1px solid #1c3050; border-radius:8px; padding:20px 24px }}
  .mv {{ font-size:2rem; font-weight:700; color:#eef2f8; font-family:monospace }}
  .mv.ok {{ color:#22d3a0 }} .mv.fail {{ color:#f43f5e }} .mv.warn {{ color:#fbbf24 }}
  .ml {{ font-size:.72rem; color:#4a6280; text-transform:uppercase; letter-spacing:.08em }}
  table {{ width:100%; border-collapse:collapse; background:#0e1829; border-radius:8px; overflow:hidden }}
  th {{ background:#132035; color:#4a6280; font-size:.72rem; text-transform:uppercase; letter-spacing:.08em; padding:10px 14px; text-align:left }}
  td {{ padding:10px 14px; border-top:1px solid #1c3050; font-size:.875rem }}
</style></head><body>
<h1>Suite de Regressão</h1>
<p class="sub">{datetime.now():%d/%m/%Y %H:%M} — {total} scripts executados</p>
<div class="metrics">
  <div class="m"><div class="mv">{total}</div><div class="ml">Total</div></div>
  <div class="m"><div class="mv ok">{passou}</div><div class="ml">PASS ({pct}%)</div></div>
  <div class="m"><div class="mv fail">{falhou}</div><div class="ml">FAIL</div></div>
  <div class="m"><div class="mv warn">{bloq}</div><div class="ml">BLOCKED</div></div>
</div>
<table>
  <tr><th>Script</th><th>Status</th><th>Duração</th></tr>
  {linhas_cts}
</table>
</body></html>"""

    dash = ev_dir / "dashboard.html"
    dash.write_text(html, encoding="utf-8")
    print(f"\n✓ Dashboard: {dash}")
    return dash

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--modulo", default=None, help="Filtrar por módulo")
    p.add_argument("--dry-run", action="store_true", help="Listar sem executar")
    args = p.parse_args()

    scripts = listar_scripts(args.modulo)
    if not scripts:
        print("Nenhum script encontrado em", REGRESSIVO_DIR)
        sys.exit(1)

    print(f"→ {len(scripts)} scripts encontrados")
    if args.dry_run:
        for s in scripts:
            print(f"  {s.name}")
        return

    ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    ev_dir = EV_BASE / f"regressivo_{ts}"
    ev_dir.mkdir(parents=True, exist_ok=True)

    resultados = []
    for script in scripts:
        print(f"\n→ Executando: {script.name}")
        r = rodar_script(script, ev_dir)
        resultados.append(r)
        print(f"  {r['status']} ({r['duracao']}s)")

    gerar_dashboard(resultados, ev_dir)

    passou = sum(1 for r in resultados if r["status"] == "PASS")
    print(f"\n{'='*50}")
    print(f"  RESULTADO FINAL: {passou}/{len(resultados)} PASS")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
