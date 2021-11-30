## In this proyect I mean to scrape data abour player statistics this season from English Premier League webpage.
## I'm going to gather information about goals, passes, minutes played, wins, losses and other information one could use to do good analysis. 


# TOOLS
# The two web scraping libraries that will help you smooth this project’s implementation is BeautifulSoup and Requests of the Python 
# programming language. They allow easy access to websites and parsing of HTML pages.



######## librerías
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

try:
    WebDriverWait(browser, 5).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[5]/button[1]')))
    
    cookies = browser.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[5]/button[1]')
    browser.execute_script("arguments[0].click();",cookies)
    time.sleep(3)
except:
    print(f"Cookies Element not located")


#------------------------------ finding and clicking to show current season players  ------------------------------------- 

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
playerRanks = []
playerNames = []
playerInfo = []
playerCountry = []
playerGoals = []
##playerClub = []


# Goals 
while True:
    
    bs = BeautifulSoup(browser.page_source, 'html.parser')
    rank = bs.find_all('td', {'class':'rank'})
    Names = bs.find_all('a', {'class':'playerName'})
    Country = bs.find_all('span', {'class':'playerCountry'})
    goals = bs.find_all('td', {'class':'mainStat text-centre'})


    for i in range(len(rank)):
        playerRanks.append(rank[i].text)
        playerNames.append(Names[i].find('strong').text)
        playerInfo.append(Names[i].attrs['href'])
        playerCountry.append(Country[i].text)
        playerGoals.append(goals[i].text) 
    

    ## getting Clubs information
    ## I have to do this process because some of the player do not have the club name in the main page
    # for ul in playerInfo:
    #     ul = f'https:{ul}'
    #     pageUl = requests.get(ul)
    #     club = BeautifulSoup(pageUl.text, 'html.parser').find('span', {'class':'long'}).text
    #     playerClub.append(club)

    ## condition to break the loop
    if (int(goals[-1].text) == 0):
        break

    try:
        WebDriverWait(browser, 3).until(
                     EC.presence_of_element_located((By.XPATH,'//*[@id="mainContent"]/div[2]/div/div[2]/div[1]/div[3]/div[2]')))

        arrow = browser.find_element_by_xpath('//*[@id="mainContent"]/div[2]/div/div[2]/div[1]/div[3]/div[2]')
        browser.execute_script("arguments[0].click();",arrow)
    except StopIteration:
       break

dictGoals = {'Rank':playerRanks, "Names": playerNames, 'Nationality':playerCountry, 'Goals':playerGoals}
dfGoals = pd.DataFrame(dictGoals, columns=['Rank', 'Names', 'Club', 'Nationality', 'Goals'])

print(dfGoals)


browser.close()


















