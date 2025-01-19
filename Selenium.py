import time
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions

path_citilink_videocard = "https://www.citilink.ru/catalog/videokarty/?sorting=price_desc"
# path_citilink_processor = https://www.citilink.ru/catalog/processory/?sorting=price_desc
# path_dns = "https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?order=6&stock=now-today-tomorrow-later-out_of_stock"

options = ChromeOptions()
options.add_argument("--headless")

driver = webdriver.Chrome()
driver.get(path_citilink_videocard)
actions = ActionChains(driver)
driver.implicitly_wait(10)

xpath_to_button = '/html/body/div[2]/div/main/section/div[2]/div/div/section/div[2]/div[3]/div/div[1]/div[2]/button/span'
xpath_to_accept_button = '/html/body/div[2]/div/div[4]/div[1]/div/div/button/span'

time.sleep(3)    
body = driver.find_element(By.XPATH ,'/html/body')
body.send_keys(Keys.END)

accept_button = driver.find_element(By.XPATH, xpath_to_accept_button)
actions.move_to_element(accept_button).click().perform()

i = 0
while i == 0:
    try:
        button = driver.find_element(By.XPATH, xpath_to_button)
        actions.move_to_element(button).click().perform()
        time.sleep(3)
    except:
        # print('pages are out')
        i = 1


i = 0
number_of_product = 0
while i == 0:
    number_of_product = number_of_product + 1
    try:
        xpath_to_product_card = f'/html/body/div[2]/div/main/section/div[2]/div/div/section/div[2]/div[2]/div[ {number_of_product} ]/div/div[2]/div[6]'        
        product_card = driver.find_element(By.XPATH, xpath_to_product_card)
        print(product_card.text)
        time.sleep(3)
        i = 1
    except:
        i = 1



xpath_to_price =        '/html/body/div[2]/div/main/section/div[2]/div/div/section/div[2]/div[2]/div[1]/div/div[2]/div[7]'
                      # '/html/body/div[2]/div/main/section/div[2]/div/div/section/div[2]/div[2]/div[1]'
                      # '/html/body/div[2]/div/main/section/div[2]/div/div/section/div[2]/div[2]/div[2]'   




# time.sleep(30)

# button.click()
# print(button.text)
    


# except:
#     print('error')
    


# bottom_menu = driver.find_element(By.XPATH, xpath_to_bottom_menu)







# element = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/section/div[2]/div/div/section/div[2]/div[3]/div')
# driver.get(path_dns)




# bottom_menu: WebElement
# product_price: WebElement


xpath_to_button = '/div[1]/div[2]/button'


# print(bottom_menu.get_attribute('innerHTML'))
# button = bottom_menu.find_element(By.XPATH, xpath_to_button)


# product_card = driver.find_element(By.XPATH, xpath_to_product_card)
# product_price = driver.find_element(By.XPATH, xpath_to_price)

# time.sleep(3)

# print(product_card.text)
# print(product_price.text)


