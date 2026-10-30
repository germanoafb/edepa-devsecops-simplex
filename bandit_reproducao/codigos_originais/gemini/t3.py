# Origem: respostas_brutas/gemini/resposta_completa.md (seção T3) — 1 bloco(s) Python, concatenados sem alteração.
import os
from werkzeug.utils import secure_filename


def salvar_upload(arquivo_file_storage, pasta_uploads: str = 'uploads') -> str:
  """Recebe um arquivo enviado pelo usuário (laudo ou planilha), sanitiza o nome e o salva na pasta de uploads.

  Retorna o caminho completo do arquivo salvo.
  """
  if not os.path.exists(pasta_uploads):
    os.makedirs(pasta_uploads)

  # Sanitiza o nome do arquivo para evitar caracteres maliciosos
  filename = secure_filename(arquivo_file_storage.filename)
  caminho_destino = os.path.join(pasta_uploads, filename)

  # Salva o arquivo no servidor
  arquivo_file_storage.save(caminho_destino)

  return caminho_destino
