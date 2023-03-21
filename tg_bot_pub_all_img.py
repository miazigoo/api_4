import os
import time
import random
import argparse
import telegram
from dotenv import load_dotenv


def get_command_line_argument(env_publish_time):
    """parse arg"""
    parser = argparse.ArgumentParser(
        description="""
        Программа публикует фотографии в Telegram канал.
        Если не указан при запуске аргумент, публикация будет проходить раз в 4 часа.
        Аргумент принимает целые и дробные числа. Указанное число - это время в часах. 
        """)
    parser.add_argument('hour', nargs='?', help='Укажите периодичность публикации: ', type=float, default=env_publish_time)
    hour = parser.parse_args().hour

    return hour


def main():
    load_dotenv()
    img_files = os.listdir('images')
    token = os.environ['TG_TOKEN']
    channel = os.environ['TG_CHANNEL_LOGIN']
    bot = telegram.Bot(token=token)
    sec_in_hour = 3600

    env_publish_time = float(os.getenv('TG_PUBLISH_TIME', default=4))
    command_line_argument = get_command_line_argument(env_publish_time)
    tg_publish_time = command_line_argument * sec_in_hour

    while True:
        for img in img_files:
            with open(f'images/{img}', 'rb') as pulish_img:
                bot.send_photo(chat_id=channel, photo=pulish_img)
            time.sleep(int(tg_publish_time))
        random.shuffle(img_files)


if __name__ == '__main__':
    main()
