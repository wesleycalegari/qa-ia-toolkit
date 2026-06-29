"""
publicar.py — publica um plano de teste no GitHub Pages

Uso:
    python publicar.py <pasta-do-plano> --sprint "Sprint N Meu-Projeto"

Exemplos:
    python publicar.py bug-001 --sprint "Sprint 1 Meu-Projeto"
    python publicar.py pbi-050 --sprint "Sprint 2 Meu-Projeto"

Pré-requisitos:
    - GIT_PAT e GIT_USER e GIT_REPO definidos no .env
    - A pasta contém index.html (e opcionalmente evidencias/)
    - O repositório GitHub Pages já existe e está configurado

Resultado:
    https://{GIT_USER}.github.io/{GIT_REPO}/{sprint-slug}/{pasta}/
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

GIT_PAT  = os.getenv("GIT_PAT")
GIT_USER = os.getenv("GIT_USER")
GIT_REPO = os.getenv("GIT_REPO", "planos-de-teste")

REPO_LOCAL = Path(f"c:/projetos/{GIT_REPO}")  # ajuste para o caminho local do repo

def slug(texto: str) -> str:
    """Converte 'Sprint 1 Meu Projeto' → 'sprint-1-meu-projeto'."""
    return texto.lower().replace(" ", "-")

def publicar(pasta_plano: str, sprint: str):
    sprint_slug = slug(sprint)
    origem = Path(pasta_plano)
    destino = REPO_LOCAL / "docs" / sprint_slug / origem.name

    if not (origem / "index.html").exists():
        print(f"Erro: {origem}/index.html não encontrado.")
        sys.exit(1)

    print(f"→ Copiando {origem} → {destino}")
    if destino.exists():
        shutil.rmtree(destino)
    shutil.copytree(origem, destino)

    print("→ Commit e push")
    os.chdir(REPO_LOCAL)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m",
        f"plano: {sprint} / {origem.name}"], check=True)

    remote = f"https://{GIT_USER}:{GIT_PAT}@github.com/{GIT_USER}/{GIT_REPO}.git"
    subprocess.run(["git", "push", remote, "main"], check=True)

    url = f"https://{GIT_USER}.github.io/{GIT_REPO}/{sprint_slug}/{origem.name}/"
    print(f"\n✓ Publicado: {url}")
    return url

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("pasta", help="Pasta do plano (ex: bug-001)")
    p.add_argument("--sprint", required=True, help="Nome da sprint (ex: 'Sprint 1 Meu-Projeto')")
    args = p.parse_args()
    publicar(args.pasta, args.sprint)
