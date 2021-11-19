# For this project, you can scrape data for any specific product available on Amazon and analyze its customers’ reviews. 
# After scraping, you can do sentiment analysis and perform the necessary statistical analysis to draw insightful conclusions.

from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import socks
import socket
import pandas as pd

## For using Tor to change my IP Address
socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
socket.socket = socks.socksocket


## Defining headers
headers = {
'authority': 'www.amazon.com',
'pragma': 'no-cache',
'cache-control': 'no-cache',
'dnt': '1',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'sec-fetch-site': 'none',
'sec-fetch-mode': 'navigate',
'sec-fetch-dest': 'document',
'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

pageUrl = 'https://www.amazon.com/-/es/port%C3%A1til-pulgadas-Altavoces-ordenador-tel%C3%A9fono/product-reviews/B088TLQR3K/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews&pageNumber=1'
session = requests.session()

## Lists
nextPagination = []
reviews = []
comments = []
stars = []

## Function to scrape data from a given Url
def getPaginations(pageUrl,session):
    try:
        url = session.get(pageUrl, headers=headers)
        bs = BeautifulSoup(url.text, 'html.parser')
        nextUrl = bs.find_all('li', {'class':'a-last'})

        # reviews
        for r in bs.find_all('a', {'data-hook':'review-title'}):
            reviews.append(r.text)

        # comments
        for c in bs.find_all('span', {'data-hook':'review-body'}):
            comments.append(c.text)

        # stars
        for s in bs.find_all('i', {'data-hook':'review-star-rating'}):
            stars.append(s.text[0:3])

        ## paginations
        for ul in nextUrl:
            ul = ul.find('a').attrs['href']
            nextPage = '{}://{}{}'.format(urlparse(pageUrl).scheme,urlparse(pageUrl).netloc,ul)
            if nextPage not in nextPagination:
                nextPagination.append(nextPage)
                getPaginations(nextPage,session)
    except:
        print('page missing')

## Printing a dataframe
getPaginations(pageUrl,session)
tbAmazonReviews = {'Title':reviews, 'Body': comments, 'Rating':stars}
tbAmazonReviewsDf = pd.DataFrame(tbAmazonReviews, columns=['Title','Body', 'Rating'])
# tbAmazonReviewsDf.to_csv('tbAmazonReviews.csv', encoding='utf-8')
print(tbAmazonReviewsDf.iloc[0:2]) 

