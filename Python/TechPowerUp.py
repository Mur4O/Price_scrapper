import time
import re
import pyodbc as db
import selenium
from random import randint
from PIL.ImagePalette import random
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
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


path_techpowerup = "https://www.techpowerup.com/gpu-specs/?q="
# https://www.techpowerup.com/gpu-specs/?q=5090
GPU_list = ['5090', '5080', '5070', '5060', '5050', '9070', '9060', '3060']


class TechPowerUp:
    def __init__(self):
        self.driver = None
        self.actions = None
        self.user_agent = None

    def fetch_data(self):
        buttons = self.driver.find_elements(By.CLASS_NAME, 'item-name')
        for button in buttons:
            try:
                self.actions.move_to_element(button).click().perform()
                time.sleep(randint(5, 10))
                '''
                    Сюда воткнуть код скраппинга
                '''
                self.driver.back()
                time.sleep(2)
            except selenium.common.exceptions.ElementNotInteractableException:
                pass
        self.driver.quit()


    def open_techpowerup(self):
        for elem in GPU_list:
            self.driver = webdriver.Chrome(service=service, options=options)
            self.actions = ActionChains(self.driver)
            self.driver.implicitly_wait(5)
            self.user_agent = ua.random
            options.add_argument(f'user-agent={self.user_agent}')

            path = path_techpowerup + elem + '&f=market_Desktop'
            try:
                self.driver.get(path)
                time.sleep(3)
            except selenium.common.exceptions.TimeoutException:
                logging.critical('ERR_CONNECT_TO_TECHPOWERUP')
                self.driver.quit()
            self.fetch_data()

TechPowerUp().open_techpowerup()