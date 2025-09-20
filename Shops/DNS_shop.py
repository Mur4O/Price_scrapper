import time
import re

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

logging.basicConfig(level=logging.INFO, filename="../py_log.log", filemode="w", format="%(asctime)s %(levelname)s %(filename)s %(message)s")
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

    def open_dns(self):
        with Timer('Открываем сайт'):
            conn_status = False

            while not conn_status:
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
                    conn_status = True

        self._fetch_data()
        self.driver.quit()

    def _fetch_data(self):
        try:
            i = True
            cnt = 0
            while i:
                try:
                    button_name = 'pagination-widget__show-more-btn'
                    body = self.driver.find_element(By.CLASS_NAME, button_name)
                    self.actions.move_to_element(body).click().perform()
                    cnt += 1
                    time.sleep(1)
                except:
                    i = False

            path_to_name = 'products-list__content'
            body = self.driver.find_element(By.CLASS_NAME, path_to_name)
            # print(body.get_attribute('innerHTML'))
            body = body.get_attribute('innerHTML')
        except NoSuchElementException:
            logging.exception('Нет указанного элемента')
            print('Нет указанного элемента')

        pattern = r'<span>\s*(Видеокарта.*?)<\/span>'
        all_cards = re.findall(pattern, body)
        print(all_cards)

        # with open('/Users/yarik/PycharmProjects/Price_scrapper/a.html', mode='w', encoding='utf-8') as f:
        #     f.write(body.get_attribute('innerHTML'))

        # time.sleep(3)
        #
        # path_to_name = '/html/body/div[2]/div/div[3]/div[2]/div[2]/div/div[2]/div/button'
        # name = self.driver.find_element(By.XPATH, path_to_name)
        # print(name)

DNS().open_dns()
