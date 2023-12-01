from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
import asyncio
import os
from config import *

client = TelegramClient(
    session='session_name',
    api_id=API_ID,
    api_hash=API_HASH,
    device_model="iPhone 13 Pro Max",
    system_version="14.8.1",
    app_version="8.4",
    lang_code="en",
    system_lang_code="en-US"
)

client.start(PHONE, PASSWORD)

sended_messages = []


def check_id(new_id, file_path='last_ids.txt'):
    try:
        with open(file_path, 'r') as file:
            existing_ids = file.read().strip().split(',')
            return str(new_id) in existing_ids
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return False
    except Exception as e:
        print(f"Произошла ошибка при чтении файла {file_path}: {e}")
        return False


def write_last_id(new_id, file_path='last_ids.txt'):
    try:
        if not check_id(new_id, file_path):
            with open(file_path, 'a') as file:
                file.write(',' + str(new_id))
            print(f"Айди {new_id} добавлен в файл {file_path}.")
        else:
            print(f"Айди {new_id} уже присутствует в файле {file_path}.")
    except Exception as e:
        print(f"Произошла ошибка при записи файла {file_path}: {e}")


async def download_photos(message, is_group):
    current_post_text = ''
    media_count = 0

    if is_group:
        messages = await client.get_messages(CHANNEL_TO_TRACK, limit=10)
        for message_check in messages:
            if message_check.grouped_id == message.grouped_id:
                await client.download_media(message_check.media, "temp_post_media/")
                media_count += 1
            if message_check.message != '':
                current_post_text = message_check.message
    else:
        await client.download_media(message.media, "temp_post_media/")

    media_files = ['temp_post_media/' + f for f in os.listdir('temp_post_media/') if
                   os.path.isfile(os.path.join('temp_post_media/', f))]

    return current_post_text, media_count, media_files


async def get_new_messages():
    async for message in client.iter_messages(CHANNEL_TO_TRACK, limit=1):
        if message.grouped_id is not None:
            if not check_id(message.grouped_id):
                return message
            else:
                return None
        elif not check_id(message.id):
            return message
        else:
            return None


async def send_message(message):
    global sended_messages
    media_files = None

    if message.grouped_id is not None:
        group_text, count, media_files = await download_photos(message, True)
        await client.send_file(entity=CHANNEL_TO_SEND, caption=group_text, file=media_files)
        write_last_id(message.grouped_id)
    else:
        if message.media:
            _, _, media_files = await download_photos(message, False)
            await client.send_message(entity=CHANNEL_TO_SEND, message=message.message, file=media_files)
        else:
            await client.send_message(entity=CHANNEL_TO_SEND, message=message.message)
        write_last_id(message.id)

    if media_files is not None:
        for file_path in media_files:
            os.remove(file_path)


async def main():
    while True:
        message_to_copy = await get_new_messages()
        if message_to_copy is not None:
            await send_message(message_to_copy)

        await asyncio.sleep(10)  # Adjust the sleep time as needed

with client:
    client.loop.run_until_complete(main())
