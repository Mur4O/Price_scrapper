import glob
import os
import sys
from IPython.display import display, HTML
import pandas
import requests
import pandas as pd
import psycopg
import selenium
import logging
import time
from time import perf_counter_ns
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service

options = ChromeOptions()
options.add_argument("--window-size=1920,1080")
# options.add_argument("--headless=new")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-extensions")
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.binary_location = '/Users/yarik/Chrome_with_Driver/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'
service = Service(executable_path="/Users/yarik/Chrome_with_Driver/chromedriver-mac-arm64/chromedriver")
driver = webdriver.Chrome(service=service,options=options)


actions = ActionChains(driver)
driver.implicitly_wait(10)

path_to_downloads = '/Users/yarik/Downloads/'
path_regard = 'https://www.regard.ru/'

try:
    driver.get(path_regard)
except selenium.common.exceptions.TimeoutException as CRITICAL:
    logging.critical('ERR_CONNECT_TO_SITILINK')
    sys.exit()

time.sleep(3)
xpath_to_body = '/html/body'
body = driver.find_element(By.XPATH, xpath_to_body)
body.send_keys(Keys.END)

time.sleep(3)
xpath_to_xlsx = '/html/body/div/div/footer/div[1]/div/div[1]/div/div[4]/div/noindex/a/span'

try:
    accept_button = driver.find_element(By.XPATH, xpath_to_xlsx)
    actions.move_to_element(accept_button).click().perform()
    time.sleep(1)
except:
    print('No excel file')



list_of_files = glob.glob(f'{path_to_downloads}*.xlsx') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)

data = {
    'ID': pd.Series(dtype='int'),
    'Manufacturer': pd.Series(dtype='str'),
    'PN': pd.Series(dtype='str'),
    'Name': pd.Series(dtype='str'),
    'Price': pd.Series(dtype='str'),
    'Warranty': pd.Series(dtype='str')
}

df = pd.DataFrame(data)

driver.close()

# xl = pd.ExcelFile(latest_file)
# for name in xl.sheet_names:
#     df = xl.parse(name)




