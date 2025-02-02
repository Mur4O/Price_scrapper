import time
from time import perf_counter_ns
import sys
import re
import psycopg
import selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions
import logging
from selenium.webdriver.chrome.service import Service

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w", format="%(asctime)s %(levelname)s %(message)s")

class Timer:
    def __init__(self):
        self.stage_name = stage_name

    def __enter__(self):
        self.start_time = perf_counter_ns()
        logging.info(f'Этап {stage_name} начат')
        return self

    def __exit__(self, type, value, traceback): # self, тип ошибки, значение, след
        elapsed_time = perf_counter_ns() - self.start_time
        logging.info(f'Этап {stage_name} выполнялся {elapsed_time / 1000000000} секунд')
        
path_citilink_videocard = "https://www.citilink.ru/catalog/videokarty/?sorting=price_desc"

options = ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless=new")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-extensions")
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.binary_location = '/Users/yarik/Chrome_with_Driver/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'
service = Service(executable_path="/Users/yarik/Chrome_with_Driver/chromedriver-mac-arm64/chromedriver")
driver = webdriver.Chrome(service=service,options=options)

actions = ActionChains(driver)
driver.implicitly_wait(10)

stage_name = 'стучимся на сайт'
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

xpath_to_accept_button = '/html/body/div[2]/div/div[4]/div[1]/div/div/button/span'

try:
    accept_button = driver.find_element(By.XPATH, xpath_to_accept_button)
    actions.move_to_element(accept_button).click().perform()
    time.sleep(1)
except NoSuchElementException:
    print('No accept cookie button')
    time.sleep(1)

xpath_to_button = '/html/body/div[2]/div/main/section/div[2]/div/div/section/div[2]/div[3]/div/div[1]/div[2]/button/span'

counter = 0
i = 0
stage_name = 'страница'
while i == 0:
    with Timer():
        try:
            counter += 1
            button = driver.find_element(By.XPATH, xpath_to_button)
            actions.move_to_element(button).click().perform()
            logging.info(f'Нажатие номер {counter}')
            time.sleep(3)
            # i = 1
        except NoSuchElementException:
            logging.info(f'Найдено {counter} страниц')
            i = 1
        except StaleElementReferenceException:
            logging.critical(f'Не успел прогрузить страницу, ставь задержку больше')

regex = re.compile(r'(?<=>)[А-Яа-яA-Za-z\s0-9]{1,}')
regex_to_price = re.compile(r'(?<=>)\d{1,}\s\d{1,}(?=<)')

stage_name = 'парсим данные'
with Timer():
    i = 0
    number_of_product = 0
    products = []
    while i == 0:
        product = []
        number_of_product += 1
        try:
            xpath_to_product_card = f'/html/body/div[2]/div/main/section/div[2]/div/div/section/div[2]/div[2]/div[{number_of_product}]/div/div[2]/div[6]/ul'
            product_card = driver.find_element(By.XPATH, xpath_to_product_card)
            xpath_to_price = f'/html/body/div[2]/div/main/section/div[2]/div/div/section/div[2]/div[2]/div[{number_of_product}]/div/div[2]/div[7]/div[1]/div[2]/span/span'
            price = driver.find_element(By.XPATH, xpath_to_price)

            product_card = product_card.get_attribute('innerHTML')
            product_card = re.findall(regex, product_card)
            product_card = product_card[1]
            product.append(product_card)

            price = price.get_attribute('innerHTML')
            price = re.findall(regex_to_price, price)
            price = price[0]
            price = price.replace(' ', '')

            product.append(int(price))
            product.append(1)
            products.append(tuple(product))

            # time.sleep(3)
            # i = 1
        except:
            i = 1

logging.warning(f'Обнаружено {len(products)} товаров')
# print(len(products))

stage_name = 'льём в бд'
with Timer():
    try:
        conn = psycopg.connect(f"postgresql://postgres@sqlserver/scrapper")
        cursor = conn.cursor()

        cursor.executemany("insert into dbo.products (Name, Price, Shop_id) VALUES (%s, %s, %s)", products)
        conn.commit()

        cursor.close()
        conn.close()
    except psycopg.OperationalError:
        logging.critical('Не удалось подключиться к бд')