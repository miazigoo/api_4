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
    parser.add_argument('count', nargs='?', help='Укажите число загружаемых картинок: ')
    count = parser.parse_args().count

    return count


def fetch_nasa_picture_of_the_day(nasa_api_key):
    """Download the picture of the day NASA APOD"""
    nasa_api_url = 'https://api.nasa.gov/planetary/apod'
    api_key = {'api_key': nasa_api_key}
    response = requests.get(nasa_api_url, params=api_key)
    response.raise_for_status()
    api_object = response.json()
    img_url = api_object['url']
    filename = get_filename_and_ext(img_url)[0]
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
    api_objects = response.json()
    imgs_path = 'images'
    images_url = []

    for pic_link in api_objects:
        if pic_link['url']:
            if not get_filename_and_ext(pic_link['url'])[1] == '':
                images_url.append(pic_link['url'])

    for num, img_url in enumerate(images_url):
        extension = get_filename_and_ext(img_url)[1]
        img_name = f'nasa_apod_{num}{extension}'
        download_img(img_url, img_name, imgs_path)


def main():
    load_dotenv()
    env = os.getenv('NASA_API_KEY')
    nasa_api_key = 'DEMO_KEY'
    if env:
        nasa_api_key = env
    if get_command_line_argument():
        count = get_command_line_argument()
        fetch_nasa_pictures(int(count), nasa_api_key)
    else:
        fetch_nasa_picture_of_the_day(nasa_api_key)


if __name__ == '__main__':
    main()