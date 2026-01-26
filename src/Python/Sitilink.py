import re
import pyodbc as db
import selenium
from fake_useragent import UserAgent
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service

from Timer import Timer
import logging

logging.basicConfig(level=logging.INFO, filename="../Other/py_log.log", filemode="a", format="%(asctime)s %(levelname)s %(filename)s %(message)s")
logging.getLogger("selenium").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)

options = ChromeOptions()
options.add_argument("--window-size=1920,1080")
# options.add_argument("--headless=new")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-extensions")
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.binary_location = '/Users/yarik/Chrome_with_Driver/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'
service = Service(executable_path="/Users/yarik/Chrome_with_Driver/chromedriver-mac-arm64/chromedriver")
ua = UserAgent()

path_citilink_videocard = "https://www.citilink.ru/catalog/videokarty/?sorting=price_desc"

class Sitilink:
    def __init__(self):
        self.driver = webdriver.Chrome(service=service, options=options)
        self.actions = ActionChains(self.driver)
        self.driver.implicitly_wait(5)
        self.user_agent = ua.random
        options.add_argument(f'user-agent={self.user_agent}')
        self.fin_list = []

    def fetch_data(self):
        with Timer('Фетчим данные'):
            xpath_to_body = '/html/body'
            body = self.driver.find_element(By.XPATH, xpath_to_body)
            # print(body.get_attribute('innerHTML'))
            body.send_keys(Keys.END)

            # Кнопка куки загораживает кнопку пролистывания
            xpath_to_acept_cookie = '/html/body/div[2]/div[1]/div[4]/div[2]/div/div/button/span'
            body = self.driver.find_element(By.XPATH, xpath_to_acept_cookie)
            self.actions.move_to_element(body).click().perform()


            # Берём кусок сайта содержащий все необходимые данные
            xpath_to_body = '/html/body/div[2]/div[1]/main/section/div[3]/div/div[3]/section/div[2]/div[2]'
            body = self.driver.find_element(By.XPATH, xpath_to_body)
            body = body.get_attribute('innerHTML')
            # print(body)

            # Парсим html на необходимые элементы
            pattern = r'data-meta-name="Snippet__title"\s+title="([^"]+)"'
            all_products = re.findall(pattern, body)
            pattern = r'<span[^>]*class="[^"]*MainPriceNumber[^"]*"[^>]*>([\d\s]+)</span>'
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
        # pass
        with Timer('Заливаем в бд'):
            conn = db.connect(
                              'driver={ODBC Driver 18 for SQL Server};'
                              'server=100.98.191.77;'
                              'database=Scrapper;'
                              'uid=sa;'
                              'pwd=Qwerty11;'
                              'encrypt=no;'
                              'TrustServerCertificate=yes;')

            data_for_insert = [(name, price, 2) for name, price in self.fin_list]

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


    def open_sitilink(self):
        with Timer('Стучимся на сайт'):
            try:
                # driver.set_page_load_timeout(1)
                self.driver.get(path_citilink_videocard)
            except selenium.common.exceptions.TimeoutException:
                logging.critical('ERR_CONNECT_TO_SITILINK')
                self.driver.quit()

        self.fetch_data()
        self.load_into_db()
        self.driver.quit()

Sitilink().open_sitilink()