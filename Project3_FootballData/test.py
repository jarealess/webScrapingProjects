import time
import requests
import selenium
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC



#-------------------------------------  config browser ------------------------------------- 

playerUrl = 'https://www.premierleague.com/stats/top/players/goals'

option = webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches", ['enable-automation'])
browser = webdriver.Chrome(executable_path='C:\webdriver\chromedriver.exe', options=option) ## path al chrome driver
browser.get(playerUrl)
time.sleep(5)



#------------------------------------- 'accepting' cookies popup  ------------------------------------- 

def funcHandleCookies(browser):
    try:
        WebDriverWait(browser, 5).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[5]/button[1]')))
        
        cookies = browser.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[5]/button[1]')
        browser.execute_script("arguments[0].click();",cookies)
        time.sleep(3)
    except:
        print(f"Cookies Element not located")


#------------------------------ finding and clicking to show current season players  ------------------------------------- 

def currentSeason(browser):
    season = browser.find_element_by_xpath('//*[@id="mainContent"]/div[2]/div/div[2]/div[1]/section/div[1]/div[2]')
    season.click()

    try:
        WebDriverWait(browser, 4).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="mainContent"]/div[2]/div/div[2]/div[1]/section/div[1]/ul/li[2]')))

        time.sleep(2)
        season2021 = browser.find_element_by_xpath('//*[@id="mainContent"]/div[2]/div/div[2]/div[1]/section/div[1]/ul/li[2]')
        browser.execute_script("arguments[0].click();",season2021)
        time.sleep(3)
    except:
        print(f"Element not located")



#------------------------------ lists to fill in with needed information ------------------------------------- 


funcHandleCookies(browser)
currentSeason(browser)

playerNames = []
playerStats = []
count=0
while True:

    try:
        WebDriverWait(browser, 3).until(
                     EC.presence_of_element_located((By.XPATH,'//*[@id="mainContent"]/div[2]/div/div[2]/div[1]/div[3]/div[2]')))

        arrow = browser.find_element_by_xpath('//*[@id="mainContent"]/div[2]/div/div[2]/div[1]/div[3]/div[2]')
        browser.execute_script("arguments[0].click();",arrow)
    except StopIteration:
       break
    
    bs = BeautifulSoup(browser.page_source, 'html.parser')
    Names = bs.find_all('a', {'class':'playerName'})
    stats_ = bs.find_all('td', {'class':'mainStat text-centre'})
    

    if Names[-1].find('strong').text in playerNames:
        break

    for i in range(len(Names)):
        playerNames.append(Names[i].find('strong').text)
        playerStats.append(stats_[i].text) 






dictGoals = {"Names": playerNames, 'MainStat':playerStats}
dfGoals = pd.DataFrame(dictGoals, columns=['Names', 'MainStat'])
print(dfGoals)


browser.close()



