import os

import telegram
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TG_TOKEN')
channel = os.getenv('TG_CHANNEL_LOGIN')
bot = telegram.Bot(token=token)

img = 'images/picture_of_the_day/Soul_Jimenez_1080.jpg'

bot.send_photo(chat_id=channel, photo=open(img, 'rb'))
print(bot.get_me())