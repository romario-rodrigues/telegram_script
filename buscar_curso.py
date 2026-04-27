"""
Script para buscar cursos no Telegram.
用法: python buscar_curso.py
"""

from utils import criar_cliente_telegram


async def main():
    print("🔍 Vasculhando conversas...")
    print("-" * 40)

    client = criar_cliente_telegram()
    await client.start()

    encontrou = False

    # Palavras-chave para buscar
    palavras_chave = ["camile", "ingles", "inglês", "bruno", "home", "assistant"]

    async for dialog in client.iter_dialogs():
        nome = dialog.name.lower() if dialog.name else ""

        for palavra in palavras_chave:
            if palavra in nome:
                print(f"✅ ENCONTRADO:")
                print(f"   Nome: {dialog.name}")
                print(f"   ID: {dialog.id}")
                print("-" * 40)
                encontrou = True
                break

    if not encontrou:
        print("❌ Nenhum curso encontrado.")
        print("   Tente enviar uma mensagem no grupo e rodar novamente.")


if __name__ == "__main__":
    with criar_cliente_telegram() as client:
        client.loop.run_until_complete(main())
