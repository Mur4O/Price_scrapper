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

path_dns_videocard = "https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?order=2&stock=now-today-tomorrow-later"

options = ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless=new")

driver = webdriver.Chrome(options)
driver.get(path_dns_videocard)
actions = ActionChains(driver)
driver.implicitly_wait(10)

time.sleep(3)
xpath_to_body = '/html/body'
body = driver.find_element(By.XPATH, xpath_to_body)
# print(body.get_attribute('innerHTML'))
body.send_keys(Keys.END)

xpath_to_button = '/html/body/div[2]/div/div[3]/div[2]/div[2]/div/div[2]/div/button'
                 # /html/body/div[2]/div/div[3]/div[2]/div[2]/div/div[5]/div/button
                 # /html/body/div[2]/div/div[3]/div[2]/div[2]/div/div[7]/div/button

i = 0
while i == 0:
    try:
        button = driver.find_element(By.XPATH, xpath_to_button)
        actions.move_to_element(button).click().perform()
        print('page')
        time.sleep(3)
        i = 1
    except:
        print('pages are out')
        i = 1

regex = re.compile(r'(?<=>)[А-Яа-яA-Za-z\s0-9]{1,}')
regex_to_price = re.compile(r'(?<=>)\d{1,}\s\d{1,}(?=<)')

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

        product.append(price)
        products.append(product)
        # print(products)
        # time.sleep(3)
        # i = 1
    except:
        i = 1

for elem in products:
    print(elem)


# conn = psycopg.connect(f"postgresql://postgres@dbserver.lan/albion")

