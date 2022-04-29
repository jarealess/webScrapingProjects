#PROJECT
#For this project, you can pick a website like Expedia or Kayak, fill in your details using automated fashion, and then crawl the 
# website to extract the price information.

#TOOL
#Python’s Selenium is suitable for performing web scraping in this project. Additionally, you can use Python’s smtplib package to 
# send an email containing the information that you extracted from the website to yourself.


##--------- libraries
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC



##--------- config browser
option = webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches", ['enable-automation'])
browser = webdriver.Chrome(executable_path='C:\webdriver\chromedriver.exe', options=option) ## path al chrome driver


#---------------- function to get flights from KAYAK

def findFlights(source,destination,i_date, f_date):


    url=("https://www.kayak.com.co/flights/{0}-{1}/{2}/{3}?sort=bestflight_a".format(source,destination,i_date, f_date))
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
            time.sleep(3)
        except:
            print(f"Element not located in iteration {i}")


    #------------- getting data
    bs = BeautifulSoup(browser.page_source, 'html.parser')
    details = bs.find_all('div', {'class':'Base-Results-HorizonResult'})

    listHorario = []
    listPrices = []
    listAirlines = []
    listStops = []
    listLinks = []

    for i in range(len(details)):

        ##--- schedule
        horario = details[i].find('div', {'class':'section times'})
        h1 = horario.find('span', {'class':'depart-time base-time'})
        h2 = horario.find('span', {'class':'arrival-time base-time'})

        if h1 is not None:
            listHorario.append('{0}-{1}'.format(h1.text,h2.text).encode('utf-8').decode())

        #--- prices 
        prices = details[i].find('div', {'class':'multibook-dropdown'})
        p1 = prices.find('span', {'class':'price-text'})
        listPrices.append(float(p1.text[2:].replace('.','')))

        #--- airlines
        airline = details[i].find('span', {'class':'codeshares-airline-names'})
        listAirlines.append(airline.text) 

        #--- stops
        flightType = details[i].find('div', {'class':'section stops'})
        f1 = flightType.find('span', {'class':'stops-text'})
        f2 = flightType.find('span', {'class':'js-layover'})

        if f2 is not None:
            listStops.append(f2.text.strip())
        else:
            listStops.append(f1.text.replace('\n',''))

        ##--- links
        fLinks = details[i].find('a', {'class':'booking-link'})
        listLinks.append('https://www.kayak.com.co{0}'.format(fLinks.attrs['href']))


    browser.close()
    
    ## dataframe
    dictFlights = {'Aerolinea':listAirlines, 'Horario':listHorario, 'Precio':listPrices, 'Escalas':listStops, 'Links':listLinks}
    dfFlights = pd.DataFrame(dictFlights, columns=['Aerolinea','Horario','Precio','Escalas','Links'])
    dfFlights = dfFlights.sort_values(by='Precio', ascending=True).drop_duplicates()

    return dfFlights




dfFlights = findFlights('MDE','ADZ','2022-03-23', '2022-03-27')

## 15 vuelos más baratos
print(dfFlights.iloc[:15])

# csv
dfFlights.to_csv('cheapestFlights.csv', encoding='utf-8', index=False, sep=';')
