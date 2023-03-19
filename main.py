from dotenv import load_dotenv
import requests
from urllib.parse import urlparse
import os
import argparse


def get_link():
    parser = argparse.ArgumentParser(description='Описание что эта программа, если получает короткую ссылку, пользователь получается количество кликов,если получается длинную ссылку - делает битлинк')
    parser.add_argument('link', help='Ваша ссылка')
    args = parser.parse_args()
    return args.link


def is_bitlink(token, bitlink):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    headers = {
      'Authorization': token,
    }
    response = requests.get(url, headers=headers)
    return response.ok


def count_clicks(token, bitlink):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    headers = {
      'Authorization': token,
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def shorten_link(token, longurl):
    url = 'https://api-ssl.bitly.com/v4/shorten'
    data = {
      'long_url': longurl,
    }
    headers = {
      'Authorization': token,
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()['link']


if __name__ == '__main__':
    load_dotenv()
    user_url = get_link()
    parsed_user_url = urlparse(user_url)
    parsed_user_url = f'{parsed_user_url.netloc}{parsed_user_url.path}'
    token_bitli = os.getenv('TOKEN')
    try:
        if is_bitlink(token_bitli, parsed_user_url):
            print(count_clicks(token_bitli, parsed_user_url))
        else:
            print(shorten_link(token_bitli, user_url))
    except requests.exceptions.HTTPError:
        print('ошибка в ссылке')
    