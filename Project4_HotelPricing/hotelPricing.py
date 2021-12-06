# Booking.com is a website that allows travellers to book hotels in various cities worldwide. 
# By scraping data from this website, you can collect information about hotels like their name, type of room, location, etc., 
# and use machine learning algorithms to train a model that learns various features of the hotels and predicts the prices

import datetime
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC


##--------- config browser
option = webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches", ['enable-automation'])
browser = webdriver.Chrome(executable_path='C:\webdriver\chromedriver.exe', options=option) ## path al chrome driver


##---------------------------------- inputs   --------------------------------------------------

destino = 'ADZ'   # iata
fechaIngreso = '2022-01-10'
fechaSalida = '2022-01-15'
n0_people = ['2','0']  # [adultos, niños]
no_rooms = '1'


#------------------- function to split date --------------------------------------------------

def split_date(fecha):
    datee = datetime.datetime.strptime(fecha, "%Y-%m-%d")
    return [datee.year, datee.month, datee.day]


#------------------- filling in URL --------------------------------------------------

url = ('https://www.booking.com/searchresults.es.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaDKIAQGYAQq4ARfIAQzYAQHoAQH4AQuIAgGoAgO4Asyvs40GwAIB0gIkZTRjOWZjOTEtZDhjYy00ZWY5LWJhMzQtMGFhNzBiNTY0M2Yw2AIG4AIB&sid'
      +'=420dd3018f25fed92757eeb7bc5adc9e&sb=1&checkin_year={0}&checkin_month={1}&checkin_monthday={2}&checkout_year={3}&checkout_month={4}&checkout_monthday={5}&group_adults={6}&group_children={7}&no_rooms={8}&map'
      +'=1&b_h4u_keep_filters=&from_sf=1&ac_langcode=es&ac_click_type=b&dest_type=city&iata={9}&#map_closed'
      ).format(split_date(fechaIngreso)[0], split_date(fechaIngreso)[1], split_date(fechaIngreso)[2], split_date(fechaSalida)[0],split_date(fechaSalida)[1],split_date(fechaSalida)[2],n0_people[0], n0_people[1], no_rooms,destino)

browser.get(url)
time.sleep(5)



#------------------- gathering information --------------------------------------------------



bs = BeautifulSoup(browser.page_source, 'html.parser')
pagination = bs.find_all('li', {'class':'ce83a38554'})

#------ lists 
titles = []
address = []
score = []
_type = []
Price = []
taxes = []
link = []


# ----- iterating throught pages
for i in range(len(pagination)):

    # ----- tarjeta de información
    card = bs.find_all('div', {'data-testid':'property-card'})

    # ----- datos 

    for j in range(len(card)):
        titles.append(card[j].find('div', {'class':'fde444d7ef'}).text)       # nombre oferta
        address.append(card[j].find('span', {'data-testid':'address'}).text)  # ciudad
        _type.append(card[j].find('span', {'class':'_c5d12bf22'}).text)       # apto / habitacion / ...
        Price.append(card[j].find('span', {'class':'fde444d7ef _e885fdc12'}).text.replace('COP','').replace('.','').strip())
        taxes.append(card[j].find('div', {'data-testid':'taxes-and-charges'}).text)  # impuestos
        link.append(card[j].find('a', {'class':'_4310f7077'}).attrs['href'])          # enlace a la oferta


        ## --score
        punts = card[j].find('div', {'class':'_9c5f726ff bd528f9ea6'})   # puntuación dada al lugar
        if punts is not None:
          score.append(punts.text)
        else:
          score.append('Sin puntos')

       
    # -- click on the '>' button
    arrow = browser.find_element_by_xpath('//*[@id="search_results_table"]/div[1]/div/div/div/div[6]/div/nav/div/div[3]/button/span')
    arrow.click()
    time.sleep(3)


    # -- next page info
    bs = BeautifulSoup(browser.page_source, 'html.parser')
      
browser.close()



# --------------- consolidado de la información   ----------------------------------

df = pd.DataFrame({'Titulos':titles, 'Ciudad':address, 'Puntuacion':score, 
                        'Tipo':_type, 'Precio':Price, 'Impuesto':taxes, 'Enlace':link}, 
                    columns=['Titulos','Ciudad','Puntuacion', 'Tipo', 'Precio', 'Impuesto', 'Enlace'])

df.to_csv('hospedaje.csv', index=False, sep=';', encoding='latin-1')

