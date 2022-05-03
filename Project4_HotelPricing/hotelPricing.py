# Booking.com is a website that allows travellers to book hotels in various cities worldwide. 
# By scraping data from this website, you can collect information about hotels like their name, type of room, location, etc., 
# and use machine learning algorithms to train a model that learns various features of the hotels and predicts the prices

import datetime
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import os
import json

mainPath = r"C:\Users\PERSONAL\Desktop\WEBSCRAPPING\webScrapingProjects"

##---------------------------------- inputs   --------------------------------------------------

destino =  input('Ingrese Ciudad (Iata): ')
fechaIngreso = input('Fecha de ingreso (yyyy-mm-dd): ')
fechaSalida = input('Fecha de salida (yyyy-mm-dd): ')
n0_people = ['2','0']  # [adultos, niños]
no_rooms = input('Ingrese número de habitaciones: ')
print('')

##--------- config browser
option = webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches", ['enable-automation'])
browser = webdriver.Chrome(executable_path='C:\webdriver\chromedriver.exe', options=option) ## path al chrome driver

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
pagination = bs.find_all('li', {'class':'f32a99c8d1'})


# ---- inicializamos lista
Hotel_Pricing = []

# ----- iterating throught pages
for i in range(int(pagination[-1].text)):

    # ----- tarjeta de información
    card = bs.find_all('div', {'data-testid':'property-card'})

    # ----- datos 
    for j in range(len(card)):
        ## inicializamos diccionario
        innerDict = {}

        innerDict['Title'] = (card[j].find('div', {'class':'fcab3ed991'}).text)       # nombre oferta
        innerDict['Type'] = (card[j].find('span', {'class':'df597226dd'}).text)       # apto / habitacion / ...
        innerDict['Price'] = (card[j].find('span', {'class':'fcab3ed991'}).text.replace('COP','').replace('.','').strip())

        ## --score
        punts = card[j].find('div', {'class':'b5cd09854e'})   # puntuación dada al lugar
        if punts is not None:
          innerDict['Score'] = (punts.text)
        else:
          innerDict['Score'] = 'Sin puntos'

        ## enlace
        innerDict['Link'] = (card[j].find('a', {'class':'e13098a59f'}).attrs['href'])          # enlace a la oferta
        
        ## insertamos en lista
        Hotel_Pricing.append(innerDict)

       
    # -- click on the '>' button

    arrow = browser.find_element_by_class_name('f32a99c8d1.f78c3700d2')
    arrow.click()
    time.sleep(3)

    # -- next page info

    bs = BeautifulSoup(browser.page_source, 'html.parser')
      
browser.close()

## --------------- almacenamos la información en un archivo .csv ---------------

if not os.path.exists(mainPath+'\Project4_HotelPricing\data'):
    os.mkdir(mainPath+'\Project4_HotelPricing\data')

filename = rf'\\hospedajes_{destino}_{fechaIngreso}_{fechaSalida}.csv'
with open(mainPath+'\Project4_HotelPricing\data'+filename, 'w', newline='') as hotelBooking:
        writer = csv.DictWriter(hotelBooking, fieldnames=list(Hotel_Pricing[0].keys()))
        writer.writeheader()
        writer.writerows(Hotel_Pricing)

# --------------- consolidado de la información   ----------------------------------

cheapest = sorted(Hotel_Pricing, key=lambda x: (x['Price'], x['Score']))[0:5]
print(json.dumps(cheapest, indent=2))
