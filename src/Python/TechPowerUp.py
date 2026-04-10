# TO-DO:
# Переписать код так, чтобы он запоминал на каком месте остановился
# Работать от обратного, искать на TechPowerUp только недостающие видяхи

import time
import re
import pyodbc as db
import selenium
import os
import shutil
from selenium.common import exceptions
from random import randint
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service

from Timer import Timer
import logging

# Выставляем рабочую директорию
base_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_path)

# Настройка логгирования для вывода как в терминал, так и в файл
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Создаем форматтер
formatter = logging.Formatter("%(asctime)s %(levelname)s %(filename)s %(message)s")

# Обработчик для вывода в терминал
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Обработчик для записи в файл (в режиме добавления)
file_handler = logging.FileHandler("./Other/py_log.log", mode="a", encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# Добавляем обработчики к логгеру
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Устанавливаем уровень логирования для конкретных библиотек
logging.getLogger("selenium").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)

# Находим предварительно добавленный в PATH Chrome
chrome_path = shutil.which("Google Chrome for Testing")

options = ChromeOptions()
options.add_argument("--window-size=1920,1080")
# options.add_argument("--headless=new")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-extensions")
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

options.add_argument("--disable-cache")
options.add_argument("--disable-application-cache")
options.add_argument("--disable-cookies")

options.binary_location = chrome_path
service = Service(executable_path="/Users/yarik/Chrome_with_Driver/chromedriver-mac-arm64/chromedriver")
ua = UserAgent()

path_techpowerup = "https://www.techpowerup.com/gpu-specs/?q="
# https://www.techpowerup.com/gpu-specs/?q=5090
GPU_list = ['RTX 5000 Ada Generation', 'RTX 5090', 'RTX 5080', 'RTX 5070 Ti', 'RTX 5070', 'RTX 5060 Ti', 'RTX 5060', 'RTX 5050', 'RTX 4070 SUPER', 'RTX 4070', 'RTX 4060', 'RTX 3060', 'RTX 3050', 'GTX 1650', 'GT 1030', 'GT 730', 'GT 710', 'GeForce 210', 'RTX A5000', 'RTX A4500', 'RTX A4000', 'Quadro T1000', 'Quadro RTX A4000', 'Radeon RX 9070 XT', 'Radeon RX 9070', 'Radeon RX 9060 XT', 'Radeon RX 7800 XT', 'Radeon RX 7700 XT', 'Radeon RX 7600 XT', 'Radeon RX 7600', 'Radeon RX 6600', 'Radeon RX 6500 XT', 'Radeon RX 6400', 'Radeon RX 550', 'Radeon R7 240', 'Radeon PRO W7900 AI TOP', 'Radeon PRO W7800 AI TOP', 'Arc B580', 'Arc B570', 'Arc A580', 'Arc A380', 'Arc A310']
# GPU_list = ['RTX 5090']
params = []

class TechPowerUp:
    def __init__(self):
        self.driver = None
        self.actions = None
        self.user_agent = None
        self.fin_list = []

    def open_techpowerup(self):
        for elem in GPU_list:
            options.add_argument(f'user-agent={self.user_agent}')
            self.driver = webdriver.Chrome(service=service, options=options)
            self.actions = ActionChains(self.driver)
            self.driver.implicitly_wait(5)
            self.user_agent = ua.random

            path = path_techpowerup + elem.replace(' ', '+')
            try:
                logging.info(f'Пробуем получить данные о {elem}')
                self.driver.get(path)
                self.driver.delete_all_cookies() 
                time.sleep(3)
            except exceptions.TimeoutException:
                logging.critical('ERR_CONNECT_TO_TECHPOWERUP')
                self.driver.quit()
            self.fetch_data(elem)
            time.sleep(3)

    def fetch_data(self, product_name: str):
        buttons = self.driver.find_elements(By.CLASS_NAME, 'item-name')
        for button in buttons:
            link = str(button.get_attribute('innerHTML'))
            if link.find(product_name) != -1:
                try:
                    self.actions.move_to_element(button).click().perform()
                    time.sleep(randint(5, 10))
                    
                    specs = []

                    name = self.driver.find_element(By.CLASS_NAME, 'gpudb-name')
                    specs.append(name.get_attribute('innerHTML'))

                    raw_specs = self.driver.find_elements(By.CLASS_NAME, 'gpudb-specs-large__value')
                    for elem in raw_specs:
                        specs.append(elem.get_attribute('innerHTML'))
                
                    self.fin_list.append(specs)

                    '''
                        Сюда воткнуть код скраппинга
                    '''
                    self.driver.back()
                    time.sleep(5)
                except exceptions.ElementNotInteractableException:
                    logging.info(f'Элемент не интерактивен для {product_name}')
                    pass
                except exceptions.NoSuchElementException:
                    logging.warning(f'NoSuchElementException для {product_name}. ')
                    time.sleep(300)
                    pass
        # logging.info(f'Список найденных спецификаций: {self.fin_list}')
        self.load_into_db()
        self.driver.quit()
        
    def load_into_db(self):
        tpu_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(tpu_dir, 'Other', 'TPU')

        with open(output_path, 'w', encoding='utf-8') as f:
            for item in self.fin_list:
                f.write(f"{item}\n")

TechPowerUp().open_techpowerup()