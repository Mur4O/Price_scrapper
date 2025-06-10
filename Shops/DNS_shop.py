import time
import sys
import re
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
# options.add_argument("--headless=new")

ua = UserAgent()
userAgent = ua.random
options.add_argument(f'user-agent={userAgent}')

options.binary_location = 'D:\Chrome_with_Driver\chrome-win64\chrome.exe'
service = Service(executable_path="D:\Chrome_with_Driver\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service,options=options)
driver.implicitly_wait(10)
actions = ActionChains(driver)

def open_dns():
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
        return True
    else:
        return False

# '<a target="_blank" rel="noopener noreferrer" href="https://www.dns-shop.ru/">DNS</a>'
# xpath_to_body = '/html/body/a'
# body = driver.find_element(By.XPATH, xpath_to_body)
# # print(body.get_attribute('innerHTML'))
# body.send_keys(Keys.END)
result_code = True

while result_code:
    result_code = open_dns()