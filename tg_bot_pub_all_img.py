import os
import time
import random
import argparse
import telegram
from dotenv import load_dotenv


def get_command_line_argument():
    """parse arg"""
    parser = argparse.ArgumentParser(
        description="""
        Программа публикует фотографии в Telegram канал.
        Если не указан при запуске аргумент, публикация будет проходить раз в 4 часа.
        Аргумент принимает целые и дробные числа. Указанное число - это время в часах. 
        """)
    parser.add_argument('hour', nargs='?', help='Укажите периодичность публикации: ', default=4)
    hour = parser.parse_args().hour

    return float(hour)


def main():
    load_dotenv()
    img_files = [f for f in os.listdir('images')]
    tg_publish_time = os.getenv('TG_PUBLISH_TIME')
    token = os.environ['TG_TOKEN']
    channel = os.environ['TG_CHANNEL_LOGIN']
    bot = telegram.Bot(token=token)
    sec_in_hour = 3600
    publish_time = get_command_line_argument() * sec_in_hour
    if tg_publish_time:
        publish_time = float(tg_publish_time) * sec_in_hour

    while True:
        for img in img_files:
            bot.send_photo(chat_id=channel, photo=open(f'images/{img}', 'rb'))
            time.sleep(int(publish_time))
        random.shuffle(img_files)


if __name__ == '__main__':
    main()
