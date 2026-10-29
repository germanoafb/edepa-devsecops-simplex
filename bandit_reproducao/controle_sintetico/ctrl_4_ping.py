# CONTROLE SINTÉTICO — NÃO é código do experimento do artigo.
# Escrito apenas para conferir o mapeamento teste -> severidade/confiança -> CWE
# do Bandit instalado. Não usar como evidência dos resultados da Tabela 2.
import os
import subprocess


def ping_subprocess(host):
    return subprocess.run("ping -c 1 " + host, shell=True)


def ping_os_system(host):
    return os.system("ping -c 1 " + host)
