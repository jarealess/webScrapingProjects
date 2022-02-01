import scrapy
import time
from selenium import webdriver



class JobportalSpider(scrapy.Spider):
    name = 'JobPortalCT'
    #allowed_domains = ['www.elempleo.com/co/ofertas-empleo/?trabajo=']
    

    def start_requests(self):

        ## link
        url = 'http://www.elempleo.com/co/ofertas-empleo/?trabajo='+self.jobarg

        yield scrapy.Request(url=url, callback=self.parse)

#'Publicado 27 Ene 2022
    def parse(self, response):

        # config Selenium
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ['enable-automation'])
        option.add_argument("headless")
        browser = webdriver.Chrome(executable_path='C:\webdriver\chromedriver.exe', options=option)
        browser.get('http://www.elempleo.com/co/ofertas-empleo/?trabajo='+self.jobarg)
        response = browser.page_source

    ##nextButton = browser.find_element_by_xpath('/html/body/div[8]/div[4]/div[1]/div[4]/div/nav/ul/li[8]/a')

        ## encontramos los empleos en la página
        jobsEE = response.xpath('//div[contains(@class, "result-list")]//div[contains(@class, "result-item")]//ul')

        i = 0
        for job in jobsEE:
            
            ## matching job Title Parameters
            jobTitle = job.xpath('./li[1]/h2/a/text()').get().replace('\r\n','').strip()
            isMatch = [True for x in getattr(self, 'jobarg2').split(',') if x in jobTitle]

            ## Matching recent days
            publishDate = job.xpath('./li[3]/span[3]').get()[120:180].replace('\r\n','').strip()

            if True in isMatch:
                i+=1 
                yield {f'Post{i}': jobTitle,
                        'Company': job.xpath('./li[2]/h3/span[2]/span/text()').get().replace('\r\n','').strip(),
                        'Salary':job.xpath('./li[3]/span[1]/text()').get().replace('\r\n','').strip(),
                        'City':job.xpath('./li[3]/span[2]/span/span[1]').get()[120:170].replace('\r\n','').strip(),
                        'Date': publishDate
                    }


            ## following page search
            next_page = ''
            if next_page is not None:
                    yield response.follow(next_page, callback=self.parse)

