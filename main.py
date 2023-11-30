from telethon import TelegramClient, events
from telethon.tl.types import PeerChannel
import telethon
from config import * 

client = TelegramClient(
    session='session_name',
    api_id=API_ID,
    api_hash=API_HASH,
    device_model="iPhone 13 Pro Max",
    system_version="14.8.1",
    app_version="8.4",
    lang_code="en",
    system_lang_code="en-US")

client.start(PHONE, PASSWORD)
last_post_date = ''

async def send_mess(message, file):
    try:
        await client.send_message(entity=CHANNEL_TO_SEND, message=message, file=file)
    except AttributeError and TypeError:
        await client.send_message(entity=CHANNEL_TO_SEND, message=message)
    except telethon.errors.rpcerrorlist.MediaCaptionTooLongError:
        caption_long_message = await client.send_message(entity=CHANNEL_TO_SEND, message=message)
        await client.send_file(entity=CHANNEL_TO_SEND, file=file, reply_to=caption_long_message)

@client.on(events.NewMessage(PeerChannel(channel_id=CHANNEL_TO_TRACK)))
async def my_event_handler(event):
    print(event.message)

client.run_until_disconnected()

1
