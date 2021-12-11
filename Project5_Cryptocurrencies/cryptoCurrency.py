#Cryptocurrency is a hot topic among investors considering its fluctuating prices. Even Tesla’s CEO, Elon Musk, tweeted about one 
# of the most popular cryptocurrencies available. Additionally, Raghu Ram Rajan, the world’s renowned economist, recently commented 
# that cryptocurrency holds a decent future and can become an effective means of payment.


#For this project, we have an exciting website for you that hosts all the relevant information for cryptocurrencies like NFT, their 
# last seven days’ trend, etc. One can find these details on CoinMarketCap.



import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver



##----- config browser  ---> se cambia dirección IP  -----------------------------
# torexe = os.popen(r'C:\Users\PERSONAL\Desktop\Tor Browser\Browser\TorBrowser\Tor\tor.exe')
# PROXY = "socks5://localhost:9050" # IP:PORT or HOST:PORT
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_experimental_option("excludeSwitches", ['enable-automation']) # options.add_argument('--proxy-server=%s' % PROXY)
driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:\webdriver\chromedriver.exe')


driver.get("https://coinmarketcap.com/?page=")
time.sleep(5)




#--------------- obtenemos la información de cada criptomoneda

bs = BeautifulSoup(driver.page_source, 'lxml')
trS = bs.find('tbody').find_all('tr')

# Buttons = bs.find('ul', {'class':'pagination'}).find_all('li', {'class':'page'})

# print(Buttons[-1].find('a').text)

for tr in trS:
    print(tr)
    print('')

    # coin1 = tr.find('div', {'class':'sc-1teo54s-1'})
    # coin2= tr.find('p', {'class':'iworPT'})
    # if coin1 is not None:    
    #     print(coin1.text)
    # else:
    #     continue

# coins = driver.find_elements_by_class_name('sc-1eb5slv-0.iworPT')

# print(len(coins))

# for coin in coins:
#     print(coin.text)




time.sleep(2)

driver.close()



