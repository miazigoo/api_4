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
    img_files = [f for f in os.listdir('images')]

    token = os.getenv('TG_TOKEN')
    channel = os.getenv('TG_CHANNEL_LOGIN')
    bot = telegram.Bot(token=token)

    if not get_command_line_argument() == None:
        img = get_command_line_argument()
    else:
        img = img_files[random.randint(0, (len(img_files)-1))]

    bot.send_photo(chat_id=channel, photo=open(f'images/{img}', 'rb'))




if __name__ == '__main__':
    main()