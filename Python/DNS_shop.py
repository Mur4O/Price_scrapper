import re
import time
from fake_useragent import UserAgent
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from Timer import Timer
import logging

import sys
import os
sys.path.append(os.path.join(sys.path[0], '../ConnectionPool.py'))
from Python import ConnectionPool as cp

logging.basicConfig(level=logging.INFO, filename="../Other/py_log.log", filemode="w", format="%(asctime)s %(levelname)s %(filename)s %(message)s")
logging.getLogger("selenium").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)

path_to_dns = "http://127.0.0.1:5000/link"

options = ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-extensions")
options.page_load_strategy = 'eager'
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.binary_location = '/Users/yarik/Chrome_with_Driver/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'
# options.add_argument("--headless=new")

service = Service(executable_path="/Users/yarik/Chrome_with_Driver/chromedriver-mac-arm64/chromedriver")
ua = UserAgent()

class DNS:
    def __init__(self):
        self.driver = None
        self.actions = None
        self.user_agent = None
        self.fin_list = []

    def fetch_data(self):
        with Timer('Фетчим данные'):
            try:
                cnt = 0
                while True:
                    try:
                        button_name = 'pagination-widget__show-more-btn'
                        body = self.driver.find_element(By.CLASS_NAME, button_name)
                        self.actions.move_to_element(body).click().perform()
                        cnt += 1
                        time.sleep(1)
                    except:
                        break

                path_to_name = 'products-list__content'
                body = self.driver.find_element(By.CLASS_NAME, path_to_name)
                # print(body.get_attribute('innerHTML'))
                body = body.get_attribute('innerHTML')
                # print(body)
            except NoSuchElementException:
                logging.exception('Нет указанного элемента')
                # print('Нет указанного элемента')

            # pattern = r'<span>\s*(Видеокарта.*?)<\/span>'
            pattern = r'<div class="catalog-product__name-wrapper">[^<]*<a[^>]*>[^<]*<span>([^<]+)</span></a>'
            all_products = re.findall(pattern, body)

            pattern = r'<div class="product-buy__price">([^<]+)</div>'
            all_prices = re.findall(pattern, body)

            cleaned_names = []
            for name in all_products:
                cleaned_name = name.replace('Видеокарта ', '')
                cleaned_names.append(cleaned_name)

            cleaned_prices = []
            for price in all_prices:
                cleaned_price = re.sub(r'[^\d]', '', price)
                try:
                    cleaned_price = int(cleaned_price)
                except:
                    cleaned_price = 0

                cleaned_prices.append(cleaned_price)

            self.fin_list = list(zip(cleaned_names, cleaned_prices))
            print(self.fin_list)

    def load_into_db(self):
        with Timer('Заливаем в бд'):
            conn = cp.ConnectionPool.connToSQL()

            data_for_insert = [(name, price, 1) for name, price in self.fin_list]

            query = '''
                        insert into dbo.RawData
                            (ProductName, Price, ShopId)
                        values 
                            (?, ?, ?)
                        '''

            cursor = conn.cursor()

            cursor.executemany(query, data_for_insert)
            conn.commit()

            cursor.close()
            conn.close()

    def open_dns(self):
        with Timer('Открываем сайт'):

            while True:
                self.driver = webdriver.Chrome(service=service, options=options)
                self.actions = ActionChains(self.driver)
                self.user_agent = ua.random
                options.add_argument(f'user-agent={self.user_agent}')

                self.driver.get(path_to_dns)

                xpath_to_button = '/html/body/a'
                button = self.driver.find_element(By.XPATH, xpath_to_button)
                self.actions.move_to_element(button).click().perform()

                time.sleep(3)
                self.driver.switch_to.window(self.driver.window_handles[1])

                path_to_403 = '/html/body'

                element = WebDriverWait(self.driver, 10).until(
                    ec.presence_of_element_located((By.XPATH, path_to_403))
                )
                head = self.driver.find_element(By.XPATH, path_to_403)
                result = head.get_attribute('innerHTML')

                x = re.findall("(Доступ к сайту www.dns-shop.ru запрещен.)", result)

                if len(x) != 0:
                    self.driver.close()
                    logging.info(f'Давай по новой')
                else:
                    break

        self.fetch_data()
        self.load_into_db()
        self.driver.quit()

DNS().open_dns()
