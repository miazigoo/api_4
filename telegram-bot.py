import os

import telegram
from dotenv import load_dotenv


load_dotenv()
token = os.getenv('TG_TOKEN')
channel = os.getenv('TG_CHANNEL_LOGIN')
bot = telegram.Bot(token=token)


bot.send_message(chat_id=channel, text="В канале ZZzz.")
print(bot.get_me())