import os
import random
import telegram
import argparse
from dotenv import load_dotenv


def get_command_line_argument():
    """parse arg"""
    parser = argparse.ArgumentParser(
        description="""
        Программа публикует указанную фотографию из директории images в Telegram канал.
        Если фотография не указана, опубликуется случайная фотография из директории images. 
        """)
    parser.add_argument('img', nargs='?', help='Укажите файл в директории images в формате img.png : ')
    img = parser.parse_args().img

    return img


def main():
    load_dotenv()
    img_files = os.listdir('images')
    img_name = random.choice(img_files)
    token = os.environ['TG_TOKEN']
    channel = os.environ['TG_CHANNEL_LOGIN']
    bot = telegram.Bot(token=token)
    command_line_argument = get_command_line_argument()
    if command_line_argument:
        img_name = command_line_argument

    with open(f'images/{img_name}', 'rb') as pulish_img:
        bot.send_photo(chat_id=channel, photo=pulish_img)


if __name__ == '__main__':
    main()
