# Origem: respostas_brutas/chatgpt/t3.md — 1 bloco(s) Python, concatenados sem alteração.
import os
import uuid
from pathlib import Path


def upload_arquivo(arquivo):
    try:
        pasta_upload = Path("uploads")
        pasta_upload.mkdir(parents=True, exist_ok=True)

        extensoes_permitidas = {".pdf", ".xlsx", ".csv"}

        extensao = Path(arquivo.filename).suffix.lower()

        if extensao not in extensoes_permitidas:
            return "Formato de arquivo não permitido."

        if not arquivo.filename:
            return "Nome de arquivo inválido."

        nome_arquivo = f"{uuid.uuid4().hex}{extensao}"

        caminho = pasta_upload / nome_arquivo

        arquivo.save(caminho)

        return f"Arquivo salvo com sucesso: {caminho}"

    except (OSError, AttributeError) as erro:
        return f"Erro no upload: {erro}"
