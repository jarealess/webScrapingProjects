#Cryptocurrency is a hot topic among investors considering its fluctuating prices. Even Tesla’s CEO, Elon Musk, tweeted about one 
# of the most popular cryptocurrencies available. Additionally, Raghu Ram Rajan, the world’s renowned economist, recently commented 
# that cryptocurrency holds a decent future and can become an effective means of payment.


#For this project, we have an exciting website for you that hosts all the relevant information for cryptocurrencies like NFT, their 
# last seven days’ trend, etc. One can find these details on CoinMarketCap.



import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import requests



# driver.get("https://www.coingecko.com/en")
time.sleep(5)

pageUrl = requests.get('https://www.coingecko.com/en?page=1')

#--------------- obtenemos la información de cada criptomoneda

bs = BeautifulSoup(pageUrl.text, 'lxml')
trS = bs.find('tbody').find_all('tr')
LastPage = bs.find_all('li', class_='page-item')[-2].text


coinList = []
sNameList = []
pricesList = []
oneHourRate = []
oneDayRate = []
sevenDaysRate = []
oneDayVolume = []
MktCap = []


for i in range(1,10):#range(1,int(LastPage)):
    
    url = ('https://www.coingecko.com/en?page='+str(i))
    pageUrl = requests.get(url)
    trS = BeautifulSoup(pageUrl.text, 'lxml').find('tbody').find_all('tr')


    for tr in trS:
        coinList.append(tr.find('a', class_='tw-hidden lg:tw-flex font-bold tw-items-center tw-justify-between').text.replace('\n',''))
        sNameList.append(tr.find('span', class_='tw-hidden d-lg-inline font-normal text-3xs ml-2').text.replace('\n','') ) 
        pricesList.append(tr.find('td', class_='td-price').find('span').text.replace('\n','').replace('$','').replace(',',''))  
        MktCap.append(tr.find('td', class_='td-market_cap').find('span').text.replace('\n','').replace('$','').replace(',','')) 


        oneH = tr.find('td', class_='td-change1h').find('span')
        oneDay = tr.find('td', class_='td-change24h').find('span')
        sevenDay = tr.find('td', class_='td-change7d').find('span')
        oneDayV = tr.find('td', class_='td-liquidity_score').find('span')

        if None not in [oneH,oneDay,sevenDay,oneDayV]:
            oneHourRate.append(oneH.text.replace('\n','').replace('%',''))
            oneDayRate.append(oneDay.text.replace('\n','').replace('%',''))
            sevenDaysRate.append(sevenDay.text.replace('\n','').replace('%',''))
            oneDayVolume.append(oneDayV.text.replace('\n','').replace('$','').replace(',',''))
        else: 
            oneHourRate.append('')
            oneDayRate.append('')
            sevenDaysRate.append('')
            oneDayVolume.append('')
    
    print(i)
    


print(MktCap)
print(len(MktCap))








