# Origem: respostas_brutas/claude/resposta_completa.md (módulo único, seção COMUM) — 1 bloco(s) Python, concatenados sem alteração.
"""
Funções utilitárias para um sistema de supervisão de secagem de grãos.

Dependência externa opcional (recomendada para T5):
    pip install defusedxml
"""

from __future__ import annotations

import hashlib
import hmac
import ipaddress
import os
import platform
import re
import secrets
import shutil
import sqlite3
import subprocess
import uuid
from pathlib import Path
from typing import BinaryIO

# ---------------------------------------------------------------------------
# Parâmetros de hash de senha (PBKDF2-HMAC-SHA256, somente biblioteca padrão)
# ---------------------------------------------------------------------------
_ALGORITMO = "pbkdf2_sha256"
_ITERACOES = 600_000          # recomendação OWASP para PBKDF2-SHA256
_TAM_SALT = 16


def _gerar_hash(senha: str, salt: bytes | None = None, iteracoes: int = _ITERACOES) -> str:
    salt = salt or secrets.token_bytes(_TAM_SALT)
    dk = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, iteracoes)
    return f"{_ALGORITMO}${iteracoes}${salt.hex()}${dk.hex()}"


def _verificar_hash(senha: str, hash_armazenado: str) -> bool:
    try:
        algoritmo, iteracoes, salt_hex, dk_hex = hash_armazenado.split("$")
        if algoritmo != _ALGORITMO:
            return False
        dk = hashlib.pbkdf2_hmac(
            "sha256", senha.encode("utf-8"), bytes.fromhex(salt_hex), int(iteracoes)
        )
        return hmac.compare_digest(dk.hex(), dk_hex)   # comparação em tempo constante
    except (ValueError, TypeError):
        return False


# Hash "falso" usado quando o usuário não existe, para que o tempo de resposta
# seja igual e não revele quais usuários estão cadastrados.
_HASH_FICTICIO = _gerar_hash(secrets.token_hex(16))
