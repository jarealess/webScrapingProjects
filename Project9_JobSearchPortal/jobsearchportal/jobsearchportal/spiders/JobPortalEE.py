import scrapy
import time
from selenium import webdriver
from bs4 import BeautifulSoup


class JobportalSpider(scrapy.Spider):
    name = 'JobPortalEE'


    def start_requests(self):

        ## link
        url = 'http://www.elempleo.com/co/ofertas-empleo/?trabajo='+self.jobSearched

        yield scrapy.Request(url=url, callback=self.parse)



    def parse(self, response):

        #"" -----------------------  config Selenium
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ['enable-automation'])
        option.add_argument("headless")
        option.add_argument('--log-level=3')
        browser = webdriver.Chrome(executable_path='C:\webdriver\chromedriver.exe', options=option)
        browser.get('http://www.elempleo.com/co/ofertas-empleo/?trabajo='+self.jobSearched)
        

        ## ----------------------- getting jobs information

        i = 0
        j = 0
        while True:
            j+=1

            ## ------------------- beautifulsoup
            bs = BeautifulSoup(browser.page_source, 'lxml')
            jobPosts = bs.find_all('div', {'class':'result-item'}) 

            ## ------------------- Parámetro de salida
            if i >= int(self.MaxResults):
                break
            if j > 30:
                break

            ## ------------------- iteración
            for job in jobPosts:

                # ---------- Palabras clave
                jobTitle = job.find('a', {'class':'text-ellipsis js-offer-title'}).text.replace('\n','').strip()
                isMatch = [True for x in getattr(self, 'keyWords').split(',') if x in jobTitle]

                # ----------- Información
                if True in isMatch:
                    yield {f'Post{i+1}': jobTitle,
                            'Company': job.find('span', {'class':'info-company-name js-offer-company'}).text.replace('\n','').strip(),
                            'Salary': job.find('span', {'class':'text-primary info-salary js-offer-salary'}).text.replace('\n','').strip(),
                            'City': job.find('span', {'class':'info-city js-offer-city'}).text.replace('\n','').strip(),
                            'Date': job.find('span', {'class':'info-publish-date pull-right js-offer-date'}).text.replace('\n','').strip(),
                            'Enlace': job.find('a', {'class':'text-ellipsis js-offer-title'}).attrs['href']            
                    }
                    i+=1

         
            ## ----------------- next page
            nextButton = browser.find_element_by_class_name('js-btn-next')
            browser.execute_script("arguments[0].click();",nextButton)
            time.sleep(2)
            


      