import datetime
import os
import requests
from dotenv import load_dotenv
from download_img import download_img


def get_epic_url_and_fetch(nasa_api_key):
    """Get an NASA EPIC url and after download them"""
    api_epic_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    nasa_api_params = {'api_key': nasa_api_key}
    response = requests.get(api_epic_url, params=nasa_api_params)
    response.raise_for_status()
    epic_daily = response.json()

    for num, img_and_img_date in enumerate(epic_daily):
        img_date = datetime.date.fromisoformat(img_and_img_date["date"].split(' ')[0]).strftime("%Y/%m/%d")
        img = img_and_img_date["image"]
        img_url = f'https://api.nasa.gov/EPIC/archive/natural/{img_date}/png/{img}.png'
        img_name = f'epic_{num}.png'

        img_response = requests.get(img_url, params=nasa_api_params)
        img_response.raise_for_status()
        imgs_path = 'images'
        download_img(img_response.url, img_name, imgs_path)


def main():
    load_dotenv()
    nasa_api_key = os.getenv('NASA_API_KEY', default='DEMO_KEY')
    get_epic_url_and_fetch(nasa_api_key)


if __name__ == '__main__':
    main()

