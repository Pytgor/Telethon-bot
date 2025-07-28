import asyncio
import json
import time
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaDocument, DocumentAttributeVideo
from telethon.tl.functions.messages import DeleteMessagesRequest
from datetime import datetime

# Tus credenciales
api_id = 24983135
api_hash = '990b1aa1329223073e0bc3fc9a62e568'

# Nombres y enlaces de los grupos
source_group = 'https://t.me/SinLimitesClub'
target_group = 'https://t.me/SinLimitesRD'

# Nombre de sesión y archivo de registro
session_name = 'reenviador_videos'
log_file = 'videos_enviados.json'

# Cantidad y pausa entre lotes
BATCH_SIZE = 75
PAUSA_ENTRE_LOTES = 8 * 60 * 60  # 8 horas

# Cargar IDs de mensajes ya enviados
def cargar_registro():
    try:
        with open(log_file, 'r') as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def guardar_registro(registro):
    with open(log_file, 'w') as f:
        json.dump(list(registro), f)

async def main():
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start()

    # Obtener entidades de los grupos
    from_chat = await client.get_entity(source_group)
    to_chat = await client.get_entity(target_group)

    enviados = cargar_registro()

    print("Iniciando el reenvío de videos...")
    async for message in client.iter_messages(from_chat, reverse=True):  # de más viejo a más nuevo
        if len(enviados) % BATCH_SIZE == 0 and len(enviados) > 0:
            print(f"Esperando 8 horas para el próximo lote... ({datetime.now().strftime('%H:%M:%S')})")
            guardar_registro(enviados)
            await asyncio.sleep(PAUSA_ENTRE_LOTES)

        # Eliminar mensajes de bienvenida
        if message.action and message.action.__class__.__name__ == 'MessageActionChatAddUser':
            try:
                await client(DeleteMessagesRequest(from_chat, [message.id]))
                print(f"Mensaje de unión eliminado: {message.id}")
            except:
                continue
            continue

        # Verificar si es un video
        if message.media and isinstance(message.media, MessageMediaDocument):
            for attr in message.media.document.attributes:
                if isinstance(attr, DocumentAttributeVideo):
                    if str(message.id) in enviados:
                        continue
                    try:
                        # Enviar sin texto, sin links y ocultando remitente
                        await client.send_file(
                            to_chat,
                            file=message.media.document,
                            caption='',  # Elimina texto
                            force_document=False,
                            supports_streaming=True
                        )
                        enviados.add(str(message.id))
                        print(f"Video reenviado: {message.id}")
                        await asyncio.sleep(2)
                    except Exception as e:
                        print(f"Error al reenviar video {message.id}: {e}")
                    break  # Solo uno por mensaje

    guardar_registro(enviados)
    print("Reenvío completo.")

# Ejecutar
asyncio.run(main())
