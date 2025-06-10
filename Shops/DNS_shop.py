import time
import sys
import re
from warnings import catch_warnings

import psycopg
import selenium
from fake_useragent import UserAgent
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions
from logger import logging

path_to_dns = "http://127.0.0.1:5000/link"

options = ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-extensions")
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.binary_location = 'D:\Chrome_with_Driver\chrome-win64\chrome.exe'
options.add_argument("--headless=new")

service = Service(executable_path="D:\Chrome_with_Driver\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(10)
actions = ActionChains(driver)
ua = UserAgent()

def open_dns():
    userAgent = ua.random
    options.add_argument(f'user-agent={userAgent}')
    driver.get(path_to_dns)
    time.sleep(3)
    xpath_to_button = '/html/body/a'
    button = driver.find_element(By.XPATH, xpath_to_button)
    actions.move_to_element(button).click().perform()

    time.sleep(3)
    driver.switch_to.window(driver.window_handles[1])

    path_to_403 = '/html/body'
    head = driver.find_element(By.XPATH, path_to_403)
    result = head.get_attribute('innerHTML')
    # print(result)

    x = re.findall("(Доступ к сайту www.dns-shop.ru запрещен.)", result)
    # print(len(x))

    if len(x) != 0:
        time.sleep(3)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.close()
        return True
    else:
        return False

result_code = True
while result_code:
    result_code = open_dns()

# В конец страницы
xpath_to_body = '/html/body'
body = driver.find_element(By.XPATH, xpath_to_body)
body.send_keys(Keys.END)

i = 0
res = True
path_to_button = f''

while i < 100:
    path_to_button = f'/html/body/div[2]/div/div[2]/div[2]/div[3]/div/div[{i}]/div/button'
    i += 1
    try:
        body = driver.find_element(By.XPATH, path_to_button)
        print(body.get_attribute('innerHTML'))
        actions.move_to_element(body).click().perform()
    except:
        print('Не угадали')
print('Страницы закончились')
# while True:
#     pass
#/html/body/div[2]/div/div[2]/div[2]/div[3]/div/div[2]/div/button
#/html/body/div[2]/div/div[2]/div[2]/div[3]/div/div[5]/div/button
#/html/body/div[2]/div/div[2]/div[2]/div[3]/div/div[7]/div/button
#/html/body/div[2]/div/div[2]/div[2]/div[3]/div/div[9]/div/button
#/html/body/div[2]/div/div[2]/div[2]/div[3]/div/div[13]/div/button

#/html/body/div[2]/div/div[2]/div[2]/div[3]/div/div[2]/div/button