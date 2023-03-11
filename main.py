import datetime

import requests
from pathlib import Path
from os.path import splitext
from os.path import split
from urllib.parse import urlsplit
from urllib.parse import unquote



def get_filename_and_ext(img_url):
    """Getting the link address and extension"""
    url_address = urlsplit(img_url).path
    encoding_url = unquote(url_address)
    filename = split(encoding_url)[-1]
    extension = splitext(filename)[-1]
    return filename, extension


def download_img(img_url, img_name, imgs_path):
    """Download the image"""
    img_path = Path(imgs_path)
    img_path.mkdir(parents=True, exist_ok=True)
    response = requests.get(img_url)
    response.raise_for_status()
    with open(f'{img_path}/{img_name}', 'wb') as file:
        file.write(response.content)


def fetch_nasa_picture_epic(img_name, img_url):
    """Download the NASA EPIC image"""
    nasa_api_params = {'api_key': 'DEMO_KEY'}
    response = requests.get(img_url, params=nasa_api_params)
    response.raise_for_status()
    imgs_path = 'epic'
    download_img(response.url, img_name, imgs_path)


def get_epic_url_and_fetch():
    """Get an NASA EPIC url and download"""
    api_epic_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    nasa_api_params = {'api_key': 'DEMO_KEY'}
    response = requests.get(api_epic_url, params=nasa_api_params)
    response.raise_for_status()
    api_object = response.json()
    images_and_dates = []

    for img_object in api_object:
        img_date = datetime.date.fromisoformat(img_object["date"].split(' ')[0]).strftime("%Y/%m/%d")
        images_and_dates.append((img_object["image"], img_date))

    for img, img_data in images_and_dates:
        img_url = f'https://api.nasa.gov/EPIC/archive/natural/{img_data}//png/{img}.png'
        img_name = f'epic_{img[-3:]}.png'

        fetch_nasa_picture_epic(img_name, img_url)


def fetch_nasa_picture_of_the_day():
    """Download the picture of the day NASA APOD"""
    nasa_api_url = 'https://api.nasa.gov/planetary/apod'
    nasa_api_params = {'api_key': 'DEMO_KEY'}
    response = requests.get(nasa_api_url, params=nasa_api_params)
    response.raise_for_status()
    api_object = response.json()
    img_url = api_object['url']
    filename = get_filename_and_ext(img_url)[0]
    imgs_path = 'images'
    download_img(img_url, filename, imgs_path)


def fetch_nasa_pictures(count):
    """Download the pictures NASA APOD"""
    nasa_api_url = 'https://api.nasa.gov/planetary/apod'
    nasa_api_params = {
        'api_key': 'DEMO_KEY',
        'count': count
    }
    response = requests.get(nasa_api_url, params=nasa_api_params)
    response.raise_for_status()
    api_objects = response.json()
    imgs_path = 'pictures'
    images_url = []

    for pic_link in api_objects:
        if pic_link['url']:
            if not get_filename_and_ext(pic_link['url'])[1] == '':
                images_url.append(pic_link['url'])

    for num, img_url in enumerate(images_url):
        extension = get_filename_and_ext(img_url)[1]
        img_name = f'nasa_apod_{num}{extension}'
        download_img(img_url, img_name, imgs_path)


def fetch_spacex_last_launch(api_url):
    """Download all images from spaceX api url """
    response = requests.get(api_url)
    response.raise_for_status()
    api_object = response.json()
    images_url = api_object["links"]['flickr']['original']
    imgs_path = 'images'

    for num, img_url in enumerate(images_url):
        extension = get_filename_and_ext(img_url)[1]
        img_name = f'spacex_{num}{extension}'
        download_img(img_url, img_name, imgs_path)





if __name__ == '__main__':
    spacex_api_url = 'https://api.spacexdata.com/v5/launches/5eb87d47ffd86e000604b38a'
    fetch_nasa_picture_of_the_day()
    fetch_spacex_last_launch(spacex_api_url)
    get_epic_url_and_fetch()
    count = 20
    fetch_nasa_pictures(count)







