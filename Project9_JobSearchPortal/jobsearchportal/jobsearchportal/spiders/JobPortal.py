import scrapy
import re

class JobportalSpider(scrapy.Spider):
    name = 'JobPortal'
    allowed_domains = ['www.elempleo.com/co/ofertas-empleo/?trabajo=']

    jobSearched = 'sql'
    start_urls = ['http://www.elempleo.com/co/ofertas-empleo/?trabajo='+jobSearched]

    def parse(self, response):
        
        jobsEE = response.xpath('//div[contains(@class, "result-list")]//div[contains(@class, "result-item")]//ul')

        i = 0
        for job in jobsEE:
            
            if self.jobSearched in job.xpath('./li[1]/h2/a/text()').get().replace('\r\n','').strip():
                i+=1 
                yield {f'Post{i}': job.xpath('./li[1]/h2/a/text()').get().replace('\r\n','').strip(),
                        'Company': job.xpath('./li[2]/h3/span[2]/span/text()').get().replace('\r\n','').strip(),
                        'Salary':job.xpath('./li[3]/span[1]/text()').get().replace('\r\n','').strip(),
                        'City':job.xpath('./li[3]/span[2]/span/span[1]').get()[120:170].replace('\r\n','').strip(),
                        'Date': job.xpath('./li[3]/span[3]').get()[120:180].replace('\r\n','').strip()
                    }
