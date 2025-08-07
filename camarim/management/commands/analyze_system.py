# core/management/commands/analyze_system.py
import os
import requests
from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
from dotenv import load_dotenv
load_dotenv()

OPENROUTER_KEY = settings.OPENROUTER_API_KEY
ENDPOINT = "https://openrouter.ai/v1/chat/completions"
MODEL = "qwen/qwen3-coder:free"

def call_qwen(prompt: str) -> str:
    resp = requests.post(
        ENDPOINT,
        headers={
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "Você é um agente que entende projetos Django e sugere funcionalidades faltantes."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.1,
        }
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

def chunk_files(root_paths, max_chars=20_000):
    chunks = []
    buffer = ""
    for path in root_paths:
        for dirpath, _, filenames in os.walk(path):
            for fn in filenames:
                if fn.endswith((".py", ".html")):
                    full = os.path.join(dirpath, fn)
                    with open(full, encoding="utf-8") as f:
                        data = f.read()
                    header = f"# Arquivo: {os.path.relpath(full, settings.BASE_DIR)}\n"
                    snippet = header + data + "\n\n"
                    if len(buffer) + len(snippet) > max_chars:
                        chunks.append(buffer)
                        buffer = snippet
                    else:
                        buffer += snippet
    if buffer:
        chunks.append(buffer)
    return chunks

class Command(BaseCommand):
    help = "Analisa o código Django e gera trechos faltantes via Qwen3-Coder."

    def handle(self, *args, **options):
        # 1) Coleta paths de todos os apps instalados
        app_paths = [app.path for app in apps.get_app_configs()]
        # 2) Divide em chunks
        chunks = chunk_files(app_paths)
        total = len(chunks)
        # 3) Para cada chunk, pergunta ao modelo
        for idx, chunk in enumerate(chunks, start=1):
            prompt = (
                f"Aqui está parte {idx}/{total} do código do projeto Django:\n\n"
                f"{chunk}\n\n"
                "1) Quais endpoints CRUD e testes estão faltando?\n"
                "2) Gere o código (views, urls, serializers, testes) para preencher essas lacunas."
            )
            self.stdout.write(self.style.MIGRATE_HEADING(f"\n=== Chunk {idx}/{total} ==="))
            try:
                resposta = call_qwen(prompt)
                self.stdout.write(resposta)
            except Exception as e:
                self.stderr.write(f"Erro na chunk {idx}: {e}")

        self.stdout.write(self.style.SUCCESS("Análise concluída! Revise as saídas acima e adapte ao seu projeto."))
