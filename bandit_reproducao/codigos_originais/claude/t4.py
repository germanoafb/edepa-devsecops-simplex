# Origem: respostas_brutas/claude/resposta_completa.md (módulo único, seção T4) — 1 bloco(s) Python, concatenados sem alteração.
# ===========================================================================
# T4 — Teste de conectividade (ping)
# ===========================================================================
_HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*$"
)


def _validar_endereco(endereco: str) -> str:
    endereco = endereco.strip()
    try:
        return str(ipaddress.ip_address(endereco))
    except ValueError:
        pass
    if _HOSTNAME_RE.fullmatch(endereco):
        return endereco
    raise ValueError(f"Endereço inválido: {endereco!r}")


def testar_conectividade(endereco: str, tentativas: int = 2, timeout_s: int = 2) -> dict:
    """
    Executa ping no equipamento de campo (CLP, sensor, inversor etc.).

    Segurança: o endereço é validado (IP ou hostname) e o comando é chamado
    como lista, sem shell — entradas como "10.0.0.1; rm -rf /" são rejeitadas.
    """
    alvo = _validar_endereco(endereco)
    tentativas = max(1, min(int(tentativas), 10))
    timeout_s = max(1, min(int(timeout_s), 10))

    ping = shutil.which("ping")
    if ping is None:
        raise RuntimeError("Comando 'ping' não encontrado no servidor.")

    if platform.system().lower() == "windows":
        cmd = [ping, "-n", str(tentativas), "-w", str(timeout_s * 1000), alvo]
    else:
        cmd = [ping, "-c", str(tentativas), "-W", str(timeout_s), alvo]

    try:
        resultado = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=tentativas * timeout_s + 5,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {"endereco": alvo, "alcancavel": False, "saida": "Tempo esgotado."}

    return {
        "endereco": alvo,
        "alcancavel": resultado.returncode == 0,
        "saida": (resultado.stdout or resultado.stderr).strip(),
    }
