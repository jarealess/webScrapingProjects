import scrapy


class JobportalSpider(scrapy.Spider):
    name = 'JobPortal'
    #allowed_domains = ['www.elempleo.com/co/ofertas-empleo/?trabajo=']


    def start_requests(self):
       # jobSearched = self.jobarg
        urls = ['http://www.elempleo.com/co/ofertas-empleo/?trabajo='+self.jobarg]
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        
        jobsEE = response.xpath('//div[contains(@class, "result-list")]//div[contains(@class, "result-item")]//ul')

        i = 0
        for job in jobsEE:

            jobTitle = job.xpath('./li[1]/h2/a/text()').get().replace('\r\n','').strip()
            isMatch = [True for x in getattr(self, 'jobarg2').split(',') if x in jobTitle]
            if True in isMatch:
                i+=1 
                yield {f'Post{i}': jobTitle,
                        'Company': job.xpath('./li[2]/h3/span[2]/span/text()').get().replace('\r\n','').strip(),
                        'Salary':job.xpath('./li[3]/span[1]/text()').get().replace('\r\n','').strip(),
                        'City':job.xpath('./li[3]/span[2]/span/span[1]').get()[120:170].replace('\r\n','').strip(),
                        'Date': job.xpath('./li[3]/span[3]').get()[120:180].replace('\r\n','').strip()
                    }

