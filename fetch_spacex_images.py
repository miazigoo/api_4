import argparse
import requests
from get_filename_and_ext import get_filename_and_ext
from download_img import download_img


def get_command_line_argument():
    """parse arg"""
    parser = argparse.ArgumentParser(
        description="""
        Программа загружает фотографии последнего запуска SpaceX.
        Если ввести id запуска, загрузит фотографии с него.
                 ВНИМАНИЕ!!!
        В последнем запуске может не быть фотографий. 
        """)
    parser.add_argument('flight_id', nargs='?', help='Укажите id запуска: ', default='latest')
    flight_id = parser.parse_args().flight_id

    return flight_id


def fetch_spacex_last_launch(spacex_launch_id):
    """Download all images from spaceX api url latest or id """
    spacex_api_url = f'https://api.spacexdata.com/v5/launches/{spacex_launch_id}'
    response = requests.get(spacex_api_url)
    response.raise_for_status()
    api_object = response.json()
    images_url = api_object["links"]['flickr']['original']
    imgs_path = 'images/SpaceX'

    for num, img_url in enumerate(images_url):
        extension = get_filename_and_ext(img_url)[1]
        img_name = f'spacex_{num}{extension}'
        download_img(img_url, img_name, imgs_path)


def main():
    spacex_launch_id = get_command_line_argument()
    fetch_spacex_last_launch(spacex_launch_id)


if __name__ == '__main__':
    main()
