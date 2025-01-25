import time
import re
import psycopg
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions



# path_citilink_videocard = "https://www.citilink.ru/catalog/videokarty/?sorting=price_desc"
# path_citilink_processor = https://www.citilink.ru/catalog/processory/?sorting=price_desc
path_dns = "https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?order=6&stock=now-today-tomorrow-later-out_of_stock"

options = ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless=new")

driver = webdriver.Chrome(options)
driver.get(path_dns)
actions = ActionChains(driver)
driver.implicitly_wait(10)

xpath_to_button = '/html/body/div[2]/div/main/section/div[2]/div/div/section/div[2]/div[3]/div/div[1]/div[2]/button/span'
xpath_to_accept_button = '/html/body/div[2]/div/div[4]/div[1]/div/div/button/span'

time.sleep(3)
xpath_to_body = '/html/body'
body = driver.find_element(By.XPATH, xpath_to_body)
# print(body.get_attribute('innerHTML'))
body.send_keys(Keys.END)

try:
    accept_button = driver.find_element(By.XPATH, xpath_to_accept_button)
    actions.move_to_element(accept_button).click().perform()
    time.sleep(1)
except:
    time.sleep(1)

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

