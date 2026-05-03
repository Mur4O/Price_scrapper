import os
import sys
import time
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

def download_images_from_tpu():

    ua = UserAgent()
    user_agent = ua.random

    url = 'https://www.techpowerup.com'
    headers = {
        "User-Agent": user_agent,
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.google.com/"
    }

    response = requests.get(f'{url}/gpu-specs/geforce-rtx-5090.c4216', headers=headers)

    if response.status_code != 200:
        print(f'Error: Received status code {response.status_code}')
        sys.exit(1)

    html_code = response.text
    soup = BeautifulSoup(html_code, 'lxml')
    elements = soup.find_all(class_='board-table-title__inner')

    card_types = []
    for elem in elements:
        link_tag = elem.find('a')
        if link_tag:
            card_types.append(
                link_tag.get('href')
            )
        else:
            # Фоллбэк, если внутри нет ссылки
            card_types.append(
                None
            )
            
    images = []
    for elem in card_types:
        response = requests.get(f'{url}{elem}', headers=headers)
        html_code = response.text
        soup = BeautifulSoup(html_code, 'lxml')
        
        if response.status_code != 200:
            print(f'Error: Received status code {response.status_code}')
            sys.exit(1)
        
        element = soup.find(class_='gpudb-large-image__item')
        print(element)
        if element:
            images.append(
                element.get('href')
            )
        else:
            # Фоллбэк, если внутри нет ссылки
            images.append(
                None
            )
        print(images)        
        
        name = soup.find(class_='gpudb-name')
        print(name.get_text())
        
        if os.path.exists(f'Assets/Products/{name.get_text()}.jpg'):
            print(f'Image for {name.get_text()} already exists. Skipping download.')
        else:
            with open(f'Assets/Products/{name.get_text()}.jpg', 'wb') as f:
                img_data = requests.get(f'{element.get("href")}').content
                f.write(img_data)

        time.sleep(20)
        
    print(images)