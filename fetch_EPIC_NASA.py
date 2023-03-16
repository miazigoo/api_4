import datetime
import os
import requests
from dotenv import load_dotenv
from download_img import download_img


def fetch_nasa_picture_epic(img_name, img_url, nasa_api_key):
    """Download the NASA EPIC image"""
    nasa_api_params = {'api_key': nasa_api_key}
    response = requests.get(img_url, params=nasa_api_params)
    response.raise_for_status()
    imgs_path = 'images'
    download_img(response.url, img_name, imgs_path)


def get_epic_url_and_fetch(nasa_api_key):
    """Get an NASA EPIC url and after download them"""
    api_epic_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    nasa_api_params = {'api_key': nasa_api_key}
    response = requests.get(api_epic_url, params=nasa_api_params)
    response.raise_for_status()
    json_object = response.json()

    for num, img_object in enumerate(json_object):
        img_date = datetime.date.fromisoformat(img_object["date"].split(' ')[0]).strftime("%Y/%m/%d")
        img = img_object["image"]
        img_url = f'https://api.nasa.gov/EPIC/archive/natural/{img_date}/png/{img}.png'
        img_name = f'epic_{num}.png'

        fetch_nasa_picture_epic(img_name, img_url, nasa_api_key)


def main():
    load_dotenv()
    nasa_api_key = os.getenv('NASA_API_KEY', default='DEMO_KEY')
    get_epic_url_and_fetch(nasa_api_key)


if __name__ == '__main__':
    main()

