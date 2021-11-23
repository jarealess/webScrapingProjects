#PROJECT
#For this project, you can pick a website like Expedia or Kayak, fill in your details using automated fashion, and then crawl the 
# website to extract the price information.

#TOOL
#Python’s Selenium is suitable for performing web scraping in this project. Additionally, you can use Python’s smtplib package to 
# send an email containing the information that you extracted from the website to yourself.


## libraries
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import numpy as np
import pandas as pd


## config browser
option = webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches", ['enable-automation'])
browser = webdriver.Chrome(executable_path='C:\webdriver\chromedriver.exe', options=option) ## path al chrome driver


## inputs
## se ingresa el código IATA del origen y destino y una fecha. 
source='BOG'
destination='MDE'
date='2021-11-24'
url=("https://www.kayak.com.co/flights/{0}-{1}/{2}?sort=bestflight_a".format(source,destination,date))
browser.get(url)


## loading more flights
## Esta sección sirve para hacer clic en el botón (ver más resultados)
for i in range(5):
    try:
        WebDriverWait(browser, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'resultsPaginator')))

        time.sleep(7)
        element = browser.find_element_by_class_name('moreButton')
        browser.execute_script("arguments[0].click();",element)
        time.sleep(3)
    except:
        print(f"Element not located in iteration {i}")


## getting data
bs = BeautifulSoup(browser.page_source, 'html.parser')
horario = bs.find_all('div', {'class':'section times'})
prices = bs.find_all('div', {'class':'multibook-dropdown'})
airline = bs.find_all('span', {'class':'codeshares-airline-names'})
flightType = bs.find_all('div', {'class':'section stops'})
fLinks = bs.find_all('a', {'class':'booking-link'})



## filling lists
minVal = min(len(horario),len(prices),len(airline),len(flightType),len(fLinks))

listHorario = []
listPrices = []
listAirlines = []
listStops = []
listLinks = []

for i in range(minVal):

    ## schedule
    h1 = horario[i].find('span', {'class':'depart-time base-time'})
    h2 = horario[i].find('span', {'class':'arrival-time base-time'})

    if h1 is not None:
        listHorario.append('{0}-{1}'.format(h1.text,h2.text).encode('utf-8').decode())

    #prices 
    p1 = prices[i].find('span', {'class':'price-text'})
    listPrices.append(float(p1.text[2:].replace('.','')))

    # airlines
    listAirlines.append(airline[i].text) 

    # stops
    f1 = flightType[i].find('span', {'class':'stops-text'})
    f2 = flightType[i].find('span', {'class':'js-layover'})

    if f2 is not None:
      listStops.append('{0}-{1}'.format(f1.text,f2.text).encode('utf-8').decode())
    else:
        listStops.append(f1.text)

    ##links
    listLinks.append('https://www.kayak.com.co{0}'.format(fLinks[i].attrs['href']))


## dataframe
dictFlights = {'Aerolinea':listAirlines, 'Horario':listHorario, 'Precio':listPrices, 'Paradas':listStops, 'Links':listLinks}
dfFlights = pd.DataFrame(dictFlights, columns=['Aerolinea','Horario','Precio','Paradas','Links'])
print(dfFlights)














