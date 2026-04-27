from telethon import TelegramClient

# ================= SEUS DADOS =================
API_ID =      
API_HASH = '' 

client = TelegramClient('sessao_romario', API_ID, API_HASH)

async def main():
    print("Listando seus grupos e canais...")
    print("-" * 30)
    
    # Lista os últimos 30 diálogos para facilitar
    async for dialog in client.iter_dialogs(limit=30):
        print(f"ID: {dialog.id} | Nome: {dialog.name}")

    print("-" * 30)

with client:
    client.loop.run_until_complete(main())
