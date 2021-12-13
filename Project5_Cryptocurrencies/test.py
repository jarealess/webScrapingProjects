

from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import time
from selenium import webdriver




option = webdriver.ChromeOptions()
option.add_argument('--log-level=3')  ## Para suprimir mensajes/advertencias en consola
option.add_experimental_option("excludeSwitches", ['enable-automation'])
browser = webdriver.Chrome(executable_path='C:\webdriver\chromedriver.exe', options=option) 


url = ('https://www.coingecko.com/en/coins/bitcoin/usd?chart=7_days#panel')
browser.get(url)

trS = BeautifulSoup(browser.page_source, 'html.parser').find('tbody').find_all('tr')

dict7dChange = {}
for tr in trS:

    # --- Date
    Date = tr.find('th').text.replace('\n','')

    # --- price in USD Dollars
    UsdPrice = tr.find_all('td')[1].text.replace('\n','').replace('$','').replace(',','')
    
    dict7dChange[Date] = UsdPrice
    print(f'{Date}: {float(UsdPrice)}')




