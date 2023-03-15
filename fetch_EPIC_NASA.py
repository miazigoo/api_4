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
    api_object = response.json()
    images_and_dates = []

    for img_object in api_object:
        img_date = datetime.date.fromisoformat(img_object["date"].split(' ')[0]).strftime("%Y/%m/%d")
        images_and_dates.append((img_object["image"], img_date))

    for img, img_data in images_and_dates:
        img_url = f'https://api.nasa.gov/EPIC/archive/natural/{img_data}//png/{img}.png'
        img_name = f'epic_{img[-3:]}.png'

        fetch_nasa_picture_epic(img_name, img_url, nasa_api_key)


def main():
    load_dotenv()
    env = os.getenv('NASA_API_KEY')
    nasa_api_key = 'DEMO_KEY'
    if env:
        nasa_api_key = env
    get_epic_url_and_fetch(nasa_api_key)
    print(nasa_api_key)


if __name__ == '__main__':
    main()

