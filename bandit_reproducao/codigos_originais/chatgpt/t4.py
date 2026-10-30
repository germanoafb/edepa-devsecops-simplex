# Origem: respostas_brutas/chatgpt/t4.md — 1 bloco(s) Python, concatenados sem alteração.
import subprocess
import ipaddress


def testar_conectividade(endereco):
    try:
        ipaddress.ip_address(endereco)

        resultado = subprocess.run(
            ["ping", "-c", "4", endereco],
            capture_output=True,
            text=True,
            timeout=10
        )

        if resultado.returncode == 0:
            return "Equipamento conectado!"

        return "Equipamento não respondeu ao ping."

    except ValueError:
        return "Endereço IP inválido."

    except subprocess.TimeoutExpired:
        return "Tempo limite de conexão excedido."

    except OSError as erro:
        return f"Erro ao executar ping: {erro}"
