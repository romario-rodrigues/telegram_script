"""
Script para baixar cursos do Telegram.
用法: python baixar.py
"""

import asyncio
import os
from utils import (
    carregar_config,
    criar_cliente_telegram,
    encontrar_pasta,
    limpar_nome_arquivo,
    criar_diretorio,
    buscar_numero_aula,
    formatar_progresso,
)


# 1. Adicionamos 'client' como parâmetro da função
async def main(client):
    # Carrega configurações
    config = carregar_config()
    curso_config = config["curso"]
    modulos = config["modulos"]
    padrao = config.get("padrao_aula", "#F(\\d+)")

    pasta_raiz = curso_config["nome"]
    target_link = curso_config["link"]

    print(f"📚 Curso: {pasta_raiz}")
    print(f"🔗 Link: {target_link}")
    print("-" * 40)

    # Conecta ao Telegram
    print("Conectando ao Telegram...")
    # REMOVIDO: a linha duplicada 'client = criar_cliente_telegram()' que causava o erro
    await client.start()

    print("Buscando o canal...")
    try:
        entity = await client.get_entity(target_link)
        print(f"✅ Canal encontrado: {entity.title}")
    except Exception as e:
        print(f"❌ Erro ao acessar canal: {e}")
        return

    print("\n🚀 Iniciando download...")
    print("=" * 40)

    total_baixados = 0
    total_existentes = 0

    # Itera sobre as mensagens
    async for message in client.iter_messages(entity, reverse=True):
        if not message.media or not message.text:
            continue

        # Busca o número da aula
        numero_aula = buscar_numero_aula(message.text, padrao)
        if not numero_aula:
            continue

        # Determina a pasta do módulo
        pasta_modulo = encontrar_pasta(numero_aula, modulos)
        caminho_dir = os.path.join(pasta_raiz, pasta_modulo)
        criar_diretorio(caminho_dir)

        # Limpa o nome do arquivo
        titulo_limpo = limpar_nome_arquivo(message.text)

        # Determina a extensão do arquivo
        extensao = ".mp4"  # padrão
        if hasattr(message.media, "photo"):
            extensao = ".jpg"

        nome_arquivo = f"F{numero_aula:03d}_{titulo_limpo}{extensao}"
        caminho_final = os.path.join(caminho_dir, nome_arquivo)

        if os.path.exists(caminho_final):
            print(f"⏭️  Já existe: {nome_arquivo}")
            total_existentes += 1
            continue

        print(f"📥 Baixando: {nome_arquivo}...")

        # Download com progresso
        def callback(current, total):
            print(formatar_progresso(current, total), end="")

        try:
            await client.download_media(
                message, file=caminho_final, progress_callback=callback
            )
            print()  # Nova linha após completar
            total_baixados += 1
        except Exception as e:
            print(f"\n❌ Erro ao baixar {nome_arquivo}: {e}")

    print("=" * 40)
    print(f"✅ Download concluído!")
    print(f"   📥 Baixados: {total_baixados}")
    print(f"   ⏭️  Já existiam: {total_existentes}")
    print(f"   📁 Pasta: {pasta_raiz}/")


if __name__ == "__main__":
    print("=" * 40)
    print("  📥 BAIXADOR DE CURSOS DO TELEGRAM")
    print("=" * 40)
    print()

    # Cria o cliente APENAS UMA VEZ aqui embaixo
    with criar_cliente_telegram() as client:
        # 2. Passa o cliente recém-criado para dentro do main
        client.loop.run_until_complete(main(client))
