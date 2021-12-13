#Cryptocurrency is a hot topic among investors considering its fluctuating prices. Even Tesla’s CEO, Elon Musk, tweeted about one 
# of the most popular cryptocurrencies available. Additionally, Raghu Ram Rajan, the world’s renowned economist, recently commented 
# that cryptocurrency holds a decent future and can become an effective means of payment.


#For this project, we have an exciting website for you that hosts all the relevant information for cryptocurrencies like NFT, their 
# last seven days’ trend, etc. One can find these details on CoinMarketCap.


#Librerías
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time



##--------- config browser
option = webdriver.ChromeOptions()
option.add_argument('--log-level=3')  ## Para suprimir mensajes/advertencias en consola
option.add_experimental_option("excludeSwitches", ['enable-automation'])
browser = webdriver.Chrome(executable_path='C:\webdriver\chromedriver.exe', options=option) 



## -------------- función para obtener información de Criptomonedas
def fnGetCryptoCoins():

  
    #----- solo se tomarrá la información de la primera página
    browser.get('https://www.coingecko.com/en?page=1')
    time.sleep(2)
    trS = BeautifulSoup(browser.page_source, 'lxml').find('tbody').find_all('tr')

   
    browser.close()
    # ------- Lists

    coinList, sNameList, pricesList, oneHourRate = [], [], [], []
    oneDayRate, sevenDaysRate, oneDayVolume, MktCap, Last7Days = [], [], [], [],[] 



    for tr in trS:
        coinList.append(tr.find('a', class_='tw-hidden lg:tw-flex font-bold tw-items-center tw-justify-between').text.replace('\n',''))
        sNameList.append(tr.find('span', class_='tw-hidden d-lg-inline font-normal text-3xs ml-2').text.replace('\n','') ) 
        pricesList.append(tr.find('td', class_='td-price').find('span').text.replace('\n',''))  
        MktCap.append(tr.find('td', class_='td-market_cap').find('span').text.replace('\n','')) 
        Last7Days.append(tr.find('td', class_='p-0 pl-2 text-center').find('a').attrs['href'])  #links


        ##---- esta información viene con algunos None
        oneH = tr.find('td', class_='td-change1h').find('span')
        oneDay = tr.find('td', class_='td-change24h').find('span')
        sevenDay = tr.find('td', class_='td-change7d').find('span')
        oneDayV = tr.find('td', class_='td-liquidity_score').find('span')


        ## ------- donde encuentre un None, no inserte
        if None not in [oneH,oneDay,sevenDay,oneDayV]:
            oneHourRate.append(oneH.text.replace('\n',''))
            oneDayRate.append(oneDay.text.replace('\n',''))
            sevenDaysRate.append(sevenDay.text.replace('\n',''))
            oneDayVolume.append(oneDayV.text.replace('\n',''))
        else: 
            oneHourRate.append('')
            oneDayRate.append('')
            sevenDaysRate.append('')
            oneDayVolume.append('')
    
    ##---- se almacenan las listas un diccionario 

    dictCrypto = {'Coin':coinList, 'Short Name':sNameList, 'Price':pricesList, '1h':oneHourRate, '24h':oneDayRate,
                        '7d':sevenDaysRate, '24h Volume':oneDayVolume, 'Marketing Cap':MktCap, 'Last 7d Trend Links':Last7Days}
    
    return dictCrypto




# --- función para obtener datos de una moneda deseada

def fnPrintCoinInfo(NameType, CoinName):

    dictCrypto = fnGetCryptoCoins()

    # ----------- se define el nombre a usar
    if NameType==1:
        _CoinNameType = 'Coin'
    else:
        _CoinNameType = 'Short Name'

    # -------- indice
    index_ = dictCrypto[_CoinNameType].index(CoinName)

    # --- se imprime información
    for key, value in dictCrypto.items():
        print(f'{key}: {value[index_]}')

    


# ---- evolutivo precio últimos 7 días

def fnPriceLastWeek(CoinName):

    # ---- url
    
    url = (f'https://www.coingecko.com/en/coins/{CoinName.lower()}/usd?chart=7_days#panel')
    browser.get(url)
    time.sleep(2)

    # ---- prices data
    trS = BeautifulSoup(browser.page_source, 'html.parser').find('tbody').find_all('tr')

    browser.close()
    dict7dChange = {}

    for tr in trS:

        # --- Date
        Date = tr.find('th').text.replace('\n','')

        # --- price in USD Dollars
        UsdPrice = tr.find_all('td')[1].text.replace('\n','').replace('$','').replace(',','')
        
        dict7dChange[Date] = UsdPrice
        print(f'{Date}: {float(UsdPrice)}')
    




#fnPrintCoinInfo(1, 'Bitcoin')
fnPriceLastWeek('Bitcoin')


