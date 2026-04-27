"""
Módulo de utilidades compartilhadas pelos scripts do Telegram.
"""

import os
import re
import yaml
from pathlib import Path
from telethon import TelegramClient
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()


def carregar_config():
    """Carrega configurações do arquivo config.yaml"""
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_credentials():
    """Retorna as credenciais do Telegram"""
    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")

    if not api_id or not api_hash:
        raise ValueError(
            "❌ Credenciais não encontradas!\n"
            "Configure o arquivo .env com API_ID e API_HASH.\n"
            "Copie .env.example para .env e preencha os valores."
        )

    return int(api_id), api_hash


def criar_cliente_telegram(nome_sessao="sessao_romario"):
    """Cria e retorna um cliente Telegram autenticado"""
    api_id, api_hash = get_credentials()
    return TelegramClient(nome_sessao, api_id, api_hash)


def encontrar_pasta(numero_aula, modulos):
    """Encontra a pasta do módulo baseado no número da aula"""
    for modulo in modulos:
        if modulo["inicio"] <= numero_aula <= modulo["fim"]:
            return modulo["nome"]
    return "00_Outros_Arquivos"


def limpar_nome_arquivo(texto):
    """Limpa caracteres inválidos para nomes de arquivo"""
    if not texto:
        return "arquivo_sem_titulo"

    # Pegar primeira linha e limitar tamanho
    primeira_linha = texto.split("\n")[0][:60]

    # Remover caracteres inválidos
    nome_limpo = re.sub(r'[\\/*?:"<>|]', "", primeira_linha).strip()

    return nome_limpo or "arquivo_sem_titulo"


def criar_diretorio(caminho):
    """Cria o diretório se não existir"""
    os.makedirs(caminho, exist_ok=True)
    return caminho


def buscar_numero_aula(texto, padrao):
    """Busca o número da aula no texto usando regex"""
    match = re.search(padrao, texto)
    if match:
        return int(match.group(1))
    return None


def formatar_progresso(current, total):
    """Formata a mensagem de progresso do download"""
    percentual = current * 100 / total if total > 0 else 0
    return (
        f"\r📥 {percentual:.1f}% ({current/1024/1024:.1f}MB / {total/1024/1024:.1f}MB)"
    )
