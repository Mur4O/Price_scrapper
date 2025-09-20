import time
from time import perf_counter_ns
import sys
import re
import psycopg
import selenium
from fake_useragent import UserAgent
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service

from Timer import Timer
import logging

logging.basicConfig(level=logging.INFO, filename="../py_log.log", filemode="a", format="%(asctime)s %(levelname)s %(filename)s %(message)s")
logging.getLogger("selenium").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
        
path_citilink_videocard = "https://www.citilink.ru/catalog/videokarty/?sorting=price_desc"

options = ChromeOptions()
options.add_argument("--window-size=1920,1080")
# options.add_argument("--headless=new")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-extensions")
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.binary_location = '/Users/yarik/Chrome_with_Driver/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'
service = Service(executable_path="/Users/yarik/Chrome_with_Driver/chromedriver-mac-arm64/chromedriver")
driver = webdriver.Chrome(service=service,options=options)

actions = ActionChains(driver)
driver.implicitly_wait(10)
ua = UserAgent()

class Sitilink:
    def __init__(self):
        self.driver = None
        self.actions = None
        self.user_agent = ua.random

    def open_sitilink(self):
        with Timer('Стучимся на сайт'):
            try:
                # driver.set_page_load_timeout(1)
                driver.get(path_citilink_videocard)
            except selenium.common.exceptions.TimeoutException as CRITICAL:
                logging.critical('ERR_CONNECT_TO_SITILINK')
                sys.exit()

    def fetch_data(self):







stage_name = 'стучимся на сайт Sitilink'
with Timer():
    try:
        # driver.set_page_load_timeout(1)
        driver.get(path_citilink_videocard)
    except selenium.common.exceptions.TimeoutException as CRITICAL:
        logging.critical('ERR_CONNECT_TO_SITILINK')
        sys.exit()

time.sleep(3)
xpath_to_body = '/html/body'
body = driver.find_element(By.XPATH, xpath_to_body)
# print(body.get_attribute('innerHTML'))
body.send_keys(Keys.END)

xpath_to_acept_cookie = '/html/body/div[2]/div[1]/div[4]/div[2]/div/div/button/span'
body = driver.find_element(By.XPATH, xpath_to_acept_cookie)
actions.move_to_element(body).click().perform()

xpath_to_button = '/html/body/div[2]/div[1]/main/section/div[3]/div/div[3]/section/div[2]/div[3]/div/div[1]/div[2]/button/span'
# История перемещения кнопки "Показать ещё"
# /html/body/div[2]/div[1]/main/section/div[2]/div/div/section/div[2]/div[3]/div/div[1]/div[2]/button/span


counter = 0
i = 0
stage_name = 'страница'
with Timer():
    while i == 0:
        try:
            counter += 1
            button = driver.find_element(By.XPATH, xpath_to_button)
            actions.move_to_element(button).click().perform()
            logging.info(f'Нажатие номер {counter}')
            time.sleep(3)
            # i = 1
        except NoSuchElementException:
            logging.info(f'Найдено {counter} страниц')
            print(f'Найдено {counter} страниц')
            i = 1
        except StaleElementReferenceException:
            logging.critical(f'Не успел прогрузить страницу, ставь задержку больше')
            print(f'Не успел прогрузить страницу, ставь задержку больше')

regex = re.compile(r'(?<=>)[А-Яа-яA-Za-z\s0-9]{1,}')
regex_to_price = re.compile(r'(?<=>)\d{1,}\s\d{1,}(?=<)')



# logging.warning(f'Обнаружено {len(products)} товаров')
driver.quit()
# print(products)

'''
stage_name = 'льём в бд'
with Timer():
    try:
        conn = psycopg.connect(f"postgresql://postgres@sqlserver/scrapper")
        cursor = conn.cursor()

        cursor.executemany("insert into dbo.regard (Name, Price, Shop_id) VALUES (%s, %s, %s)", products)
        conn.commit()

        cursor.close()
        conn.close()
    except psycopg.OperationalError:
        logging.critical('Не удалось подключиться к бд')'''
