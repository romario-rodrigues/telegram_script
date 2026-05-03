"""
Script para baixar cursos do Telegram.
用法: python baixar.py
"""

import os

# Lembre-se de garantir que o 'notificar_telegram' está importado aqui junto com as outras funções do utils
from utils import (
    carregar_config,
    criar_cliente_telegram,
    buscar_numero_aula,
    encontrar_pasta,
    criar_diretorio,
    limpar_nome_arquivo,
    formatar_progresso,
    notificar_telegram,
)


async def main(client):
    # Carrega configurações
    config = carregar_config()
    curso_config = config["curso"]
    modulos = config["modulos"]
    padrao = config.get("padrao_aula", "#F(\\d+)")

    pasta_raiz = curso_config["nome"]
    target_link = curso_config["link"]

    # Extrai o nome do curso para ficar mais bonito na notificação
    nome_curso = pasta_raiz.split("/")[-1]

    print(f"📚 Curso: {pasta_raiz}")
    print(f"🔗 Link: {target_link}")
    print("-" * 40)

    # Conecta ao Telegram
    print("Conectando ao Telegram...")
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

    # 1. Alerta de Início no Telegram
    await notificar_telegram(
        client,
        f"🚀 **Iniciando Download**\n\n📚 Curso: {nome_curso}\n💻 Servidor: Raspberry Pi",
    )

    total_baixados = 0
    total_existentes = 0

    try:
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

                # 2. Alerta de Arquivo Concluído no Telegram
                await notificar_telegram(client, f"✅ **Baixado:** {nome_arquivo}")

            except Exception as e:
                print(f"\n❌ Erro ao baixar {nome_arquivo}: {e}")
                # 3. Alerta de Erro Específico (ex: arquivo corrompido no Telegram)
                await notificar_telegram(
                    client, f"⚠️ **Erro ao baixar o arquivo:** {nome_arquivo}\n`{e}`"
                )

        # 4. Alerta de Conclusão da Trilha
        resumo_final = f"🏁 **Download Finalizado!**\n\n📚 Curso: {nome_curso}\n📥 Novos baixados: {total_baixados}\n⏭️ Já existiam: {total_existentes}"
        await notificar_telegram(client, resumo_final)

        print("=" * 40)
        print(f"✅ Download concluído!")
        print(f"   📥 Baixados: {total_baixados}")
        print(f"   ⏭️  Já existiam: {total_existentes}")
        print(f"   📁 Pasta: {pasta_raiz}/")

    except Exception as e:
        # 5. Alerta de Desastre Crítico (ex: Raspberry perdeu a internet ou HD encheu)
        erro_fatal = f"❌ **FALHA CRÍTICA NO SCRIPT** ❌\n\nO servidor Raspberry Pi interrompeu o download do curso **{nome_curso}**.\n\n**Erro reportado:**\n`{e}`"
        await notificar_telegram(client, erro_fatal)
        raise e  # Levanta o erro para você também ver no log do tmux


if __name__ == "__main__":
    print("=" * 40)
    print("  📥 BAIXADOR DE CURSOS DO TELEGRAM")
    print("=" * 40)
    print()

    # Cria o cliente APENAS UMA VEZ aqui embaixo
    with criar_cliente_telegram() as client:
        # Passa o cliente recém-criado para dentro do main
        client.loop.run_until_complete(main(client))
