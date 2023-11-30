from telethon import TelegramClient, events
from telethon.tl.types import PeerChannel
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

last_post_group_id = ''
current_mes_text = ''
current_post_id = 0

current_post = []
async def send_mess():
    global current_mes_text
    try:
        await client.send_message(entity=CHANNEL_TO_SEND, message=current_mes_text, file=current_post)
    except AttributeError and TypeError:
        await client.send_message(entity=CHANNEL_TO_SEND, message=current_mes_text)
    current_post.clear()
    current_mes_text = ''

@client.on(events.Album(chats=CHANNEL_TO_TRACK))
async def handler(event):
    print(1)

    await event.delete()

    raise events.StopPropagation

@client.on(events.NewMessage(PeerChannel(channel_id=CHANNEL_TO_TRACK)))
async def my_event_handler(event):

    print(2)
    global last_post_group_id
    global current_mes_text
    global current_post_id
    print(event.message.grouped_id)

    if event.message.grouped_id == last_post_group_id or last_post_group_id == '':
        current_post.append(event.message.media)
        if event.message.message != '':
            current_mes_text = event.message.message
            current_post_id = event.message.fwd_from.channel_post
        post = await client.get_messages(event.message.fwd_from.from_id.channel_id,
                                         ids=event.message.fwd_from.channel_post)
        print(event.message.fwd_from.channel_post)
        print(post)
        print('added')
    else:
        await send_mess()
        print('sended')
    last_post_group_id = event.message.grouped_id



client.run_until_disconnected()

