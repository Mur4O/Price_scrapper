import glob
import os
import sys
import pyodbc as db
import requests
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
import re

'''

options = ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless=new")
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
    logging.critical('ERR_CONNECT_TO_REGARD')
    sys.exit()

time.sleep(1)
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

time.sleep(3)
driver.close()



path_to_downloads = '/Users/yarik/Downloads/'
list_of_files = glob.glob(f'{path_to_downloads}*.xlsx') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)

'''



url = 'https://www.regard.ru/api/price/regard_price_100425_8.xlsx'
r = requests.get(url, allow_redirects=True)
with open('./price.xlsx', 'wb') as f:
    f.write(r.content)

latest_file = '/Users/yarik/PycharmProjects/Price_scrapper/price.xlsx'

Regard_excel = pd.read_excel(latest_file) #, nrows=100)
# display(Regard_excel.to_string())

Reg_excel = Regard_excel[['Unnamed: 5', 'Unnamed: 6']]
not_null_mask = Reg_excel.notnull().all(axis=1)
Reg_excel = Reg_excel[not_null_mask]

Reg_excel.rename(columns={'Unnamed: 5': 'Name', 'Unnamed: 6': 'Price'}, inplace=True)

Regard_CPU = Reg_excel[Reg_excel['Name'].str.contains(r'Процессор[ \w()]{0,}')].reset_index(drop=True)
Regard_GPU = Reg_excel[Reg_excel['Name'].str.contains(r'Видеокарта[ \w()]{0,}')].reset_index(drop=True)
# Regard_GPU.reset_index(drop=True, inplace=True)

display(Regard_GPU.to_string())







Fin_recordset = []

# for row in Reg_excel.itertuples(index=False):
#     Fin_recordset.append(row)

Fin_recordset = list(Reg_excel.itertuples(index=False, name=None))


conn = db.connect(''
                  'driver={ODBC Driver 18 for SQL Server};'
                  'SERVER=sqlserver;'
                  'database=Scrapper;'
                  'uid=sa;'
                  'pwd=Qwerty11;'
                  'encrypt=no;'
                  'TrustServerCertificate=yes;')

query = '''
insert into dbo.Regard
(name,price)
values 
(?, ?)
'''

# print(Fin_recordset[100])

# cursor = conn.cursor()
# cursor.executemany(query, Fin_recordset)
# cursor.commit()
#
# # print(cursor.fetchall())
#
# cursor.close()
# conn.close()