# TelegramPostsParser

It parses the latest news from the channel without using forwarding, so the script can work even with channels where forwarding is prohibited.

### Installation

1. Clone the repo

   ```bash
   $ git clone https://github.com/xartd0/django-simple-retro-notes.git
   ```
2. Install the requirements

   ```bash
   $ pip3 install telethon
   ```
3. Specify your data in the config

   ```bash
    PASSWORD = '' #Your password from 2fa
    PHONE = '' #Your phone number
    
    API_ID = '' #from https://my.telegram.org/auth
    API_HASH = '' #from https://my.telegram.org/auth
    
    CHANNEL_TO_SEND = #The ID of the channel that will be monitored for forwarding messages
    CHANNEL_TO_TRACK = #ID of the channel to which the posts will be sent
   ```
4. Start script

   ```bash
   $ python3 main.py
   ```

