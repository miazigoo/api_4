import requests
import argparse
import os
from dotenv import load_dotenv
from get_filename_and_ext import get_filename_and_ext
from download_img import download_img


def get_command_line_argument():
    """parse arg"""
    parser = argparse.ArgumentParser(
        description="""
        Программа загружает фотографию - "Картинка дня".
        При указании в аргументах числа, программа загрузит указанное кол-во картинок 
        """)
    parser.add_argument('count', nargs='?', type=int,
                        help='Укажите число загружаемых картинок: ')
    count = parser.parse_args().count

    return count


def fetch_nasa_picture_of_the_day(nasa_api_key):
    """Download the picture of the day NASA APOD"""
    nasa_api_url = 'https://api.nasa.gov/planetary/apod'
    api_key = {'api_key': nasa_api_key}
    response = requests.get(nasa_api_url, params=api_key)
    response.raise_for_status()
    img_url = response.json()['url']
    filename, _ = get_filename_and_ext(img_url)
    imgs_path = 'images'
    download_img(img_url, filename, imgs_path)


def fetch_nasa_pictures(count, nasa_api_key):
    """Download the pictures NASA APOD"""
    nasa_api_url = 'https://api.nasa.gov/planetary/apod'
    nasa_api_params = {
        'api_key': nasa_api_key,
        'count': count
    }
    response = requests.get(nasa_api_url, params=nasa_api_params)
    response.raise_for_status()
    img_urls = response.json()
    imgs_path = 'images'

    for num, pic_link in enumerate(img_urls):
        img_url = pic_link['url']
        _, extension = get_filename_and_ext(img_url)
        if not img_url:
            continue
        if not extension:
            continue
        img_name = f'nasa_apod_{num}{extension}'
        download_img(img_url, img_name, imgs_path)


def main():
    load_dotenv()
    nasa_api_key = os.getenv('NASA_API_KEY', default='DEMO_KEY')
    count = get_command_line_argument()
    if count:
        fetch_nasa_pictures(count, nasa_api_key)
    else:
        fetch_nasa_picture_of_the_day(nasa_api_key)


if __name__ == '__main__':
    main()
