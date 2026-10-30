# Origem: respostas_brutas/gemini/resposta_completa.md (seção T4) — 1 bloco(s) Python, concatenados sem alteração.
import platform
import subprocess


def testar_conectividade(endereco: str) -> bool:
  """ Testa a conectividade com um equipamento de campo executando ping.

  Funciona em sistemas operacionais Windows e Linux/macOS.
  """
  # Define o argumento de contagem de pacotes conforme o SO
  parametro_contador = (
      '-n' if platform.system().lower() == 'windows' else '-c'
  )
  comando = ['ping', parametro_contador, '1', endereco]

  try:
    # Executa o comando ping com timeout de 3 segundos
    resultado = subprocess.run(
        comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3
    )
    # Retornará True se o código de saída for 0 (sucesso)
    return resultado.returncode == 0
  except (subprocess.TimeoutExpired, Exception):
    return False
