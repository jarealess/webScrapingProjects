#PROJECT
#For this project, you can pick a website like Expedia or Kayak, fill in your details using automated fashion, and then crawl the 
# website to extract the price information.

#TOOL
#Python’s Selenium is suitable for performing web scraping in this project. Additionally, you can use Python’s smtplib package to 
# send an email containing the information that you extracted from the website to yourself.


##--------- libraries
import time
from bs4 import BeautifulSoup
from pymysql import MySQLError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import os
import csv
import json

mainPath = r"C:\Users\PERSONAL\Desktop\WEBSCRAPPING\webScrapingProjects"

##--------- config browser
option = webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches", ['enable-automation'])
browser = webdriver.Chrome(executable_path='C:\webdriver\chromedriver.exe', options=option) ## path al chrome driver


#---------------- function to get flights from KAYAK

def findFlights(source,destination,s_date, e_date):


    url=(f'https://www.kayak.com.co/flights/{source}-{destination}/{s_date}/{e_date}?sort=bestflight_a')
    browser.get(url)


    #---------------------- loading more flights
    #---------------------- Esta sección sirve para hacer clic en el botón (ver más resultados)
    for i in range(5):
        try:
            WebDriverWait(browser, 5).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'resultsPaginator')))

            time.sleep(7)
            element = browser.find_element_by_class_name('moreButton')
            browser.execute_script("arguments[0].click();",element)
            print('Cargando más vuelos...')
            time.sleep(3)
        except:
            print(f"Element not located in iteration {i}")


    #------------- getting data
    bs = BeautifulSoup(browser.page_source, 'html.parser')
    details = bs.find_all('div', {'class':'Base-Results-HorizonResult'})

    list_Vuelos = []
    for i in range(len(details)):
        #### En este almacenaremos info en cada iteración
        dictTickets = {}  

        ##--- schedule
        horario = details[i].find('div', {'class':'section times'})
        h1 = horario.find('span', {'class':'depart-time base-time'})
        h2 = horario.find('span', {'class':'arrival-time base-time'})

        if h1 is not None:
            dictTickets['horario'] = ('{0}-{1}'.format(h1.text,h2.text).encode('utf-8').decode())

        #--- prices 
        prices = details[i].find('div', {'class':'multibook-dropdown'})
        p1 = prices.find('span', {'class':'price-text'})
        dictTickets['precio'] = (float(p1.text[2:].replace('.','')))

        #--- airlines
        airline = details[i].find('span', {'class':'codeshares-airline-names'})
        dictTickets['aerolinea'] = (airline.text) 

        #--- stops
        flightType = details[i].find('div', {'class':'section stops'})
        f1 = flightType.find('span', {'class':'stops-text'})
        f2 = flightType.find('span', {'class':'js-layover'})

        if f2 is not None:
            dictTickets['paradas'] = (f2.text.strip())
        else:
            dictTickets['paradas'] = (f1.text.replace('\n',''))

        ##--- links
        fLinks = details[i].find('a', {'class':'booking-link'})
        dictTickets['enlace'] = ('https://www.kayak.com.co{0}'.format(fLinks.attrs['href']))

        ## Se inserta diccionario en lista
        list_Vuelos.append(dictTickets)
        


    browser.close()
    

    ##  almacenamos la información en un archivo .csv
    if not os.path.exists(mainPath+'\Project2_TicketPriceAnalysis\data'):
        os.mkdir(mainPath+'\Project2_TicketPriceAnalysis\data')

    filename = rf'\\vuelos{source}_{destination}_{s_date}_{e_date}.csv'
    with open(mainPath+'\Project2_TicketPriceAnalysis\data'+filename, 'w', newline='') as vuelosKayak:
            writer = csv.DictWriter(vuelosKayak, fieldnames=list(list_Vuelos[0].keys()))
            writer.writeheader()
            writer.writerows(list_Vuelos)
    ## dataframe
    return list_Vuelos


listFlights = sorted(findFlights('MDE','ADZ','2022-06-01', '2022-06-07'), key=lambda x: x['precio'])

## 5 vuelos más baratos
print(json.dumps(listFlights[:5], indent=2))
