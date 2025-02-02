import time
import sys
import re
import psycopg
import selenium
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions
from logger import logging
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
import selenium.webdriver.support.ui as ui
import random
from random import randint

options = ChromeOptions()
options.add_argument("--window-size=1920,1080")
# options.add_argument("--headless=new")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-extensions")
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument(f'user-agent={UserAgent()}')
options.binary_location = '/Users/yarik/Chrome_with_Driver/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'
service = Service(executable_path="/Users/yarik/Chrome_with_Driver/chromedriver-mac-arm64/chromedriver")

url_google = 'https://www.google.com/'
path_dns_videocard = "https://www.google.com?q=python#q=python"

driver = webdriver.Chrome(service=service,options=options)
driver.maximize_window()
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.get(url_google)
actions = ActionChains(driver)
driver.implicitly_wait(10)

first_result = driver.find_element(By.XPATH, '/html/body')
main_window = driver.current_window_handle
time.sleep(1)
# first_result.send_keys(Keys.COMMAND + 'w')
# driver.execute_script("window.open('https://google.com');")
time.sleep(20)
driver.switch_to.window(driver.window_handles[1])
time.sleep(1)
search_bar = '/html/body/ntp-app//div/div[2]/cr-searchbox//div/input'
time.sleep(5)
driver.find_element(By.XPATH, search_bar).send_keys('d')
time.sleep(random.randint(1,3))
driver.find_element(By.XPATH, search_bar).send_keys('n')
time.sleep(random.randint(1,3))
driver.find_element(By.XPATH, search_bar).send_keys('s')
time.sleep(random.randint(1,3))
driver.find_element(By.XPATH, search_bar).send_keys('.')
time.sleep(random.randint(1,3))
driver.find_element(By.XPATH, search_bar).send_keys('r')
time.sleep(random.randint(1,3))
driver.find_element(By.XPATH, search_bar).send_keys('u')
time.sleep(random.randint(1,3))
driver.find_element(By.XPATH, search_bar).send_keys(Keys.ENTER)
time.sleep(random.randint(1,3))
# , Keys.ENTER
first_link = '/html/body/div/div[4]/div/div[1]/a'
time.sleep(random.randint(1,3))
driver.find_element(By.XPATH, first_link).click()
while True:
    pass

# /html/body/ntp-app//div/div[2]/cr-searchbox//div/input





time.sleep(1)

time.sleep(1)


driver.find_element(By.XPATH, search_bar).send_keys('dns.ru', Keys.ENTER)


print('keys sent')



