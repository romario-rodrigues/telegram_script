"""
Script para listar todos os chats do Telegram.
用法: python listar_tudo.py
"""

from utils import criar_cliente_telegram


async def main():
    print("📋 Gerando lista de chats...")
    print("-" * 40)

    client = criar_cliente_telegram()
    await client.start()

    # Cria arquivo para salvar a lista
    arquivo_saida = "lista_chats.txt"

    with open(arquivo_saida, "w", encoding="utf-8") as arquivo:
        async for dialog in client.iter_dialogs():
            linha = f"Nome: {dialog.name} | ID: {dialog.id}\n"
            arquivo.write(linha)

            # Mostra na tela se parecer com curso
            if dialog.name and ("Camile" in dialog.name or "Ingles" in dialog.name):
                print(f"📌 {linha.strip()}")

    print("-" * 40)
    print(f"✅ Lista salva em '{arquivo_saida}'")
    print("   Use Ctrl+F para buscar")


if __name__ == "__main__":
    with criar_cliente_telegram() as client:
        client.loop.run_until_complete(main())
