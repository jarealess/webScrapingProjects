import scrapy


class JobportalSpider(scrapy.Spider):
    name = 'JobPortalCT'
    counter = 1

    def start_requests(self):

        ## link
        url = f'https://www.computrabajo.com.co/trabajo-de-{self.jobSearched}?by=publicationtime&p=1'

        yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):


        schema = 'https://www.computrabajo.com.co'

        if self.counter <= int(self.MaxResults): 
        ## encontramos los empleos en la página
            jobsCT = response.xpath('//article[contains(@class, "box_border")]')

            for job in jobsCT: 
                        
                ## matching job Title Parameters
                jobTitle = job.xpath('.//h1/a/text()').get().replace('\r\n','').strip()
                isMatch = [True for x in getattr(self, 'keyWords').split(',') if x in jobTitle.split(' ')]

                ## Company
                if job.xpath('.//p[1]/a/text()').get() is None:
                    Company = 'Unknown'
                else:
                    Company = job.xpath('.//p[1]/a/text()').get().replace('\r\n','').strip()

                ## getting items
                if self.counter <= int(self.MaxResults) and True in isMatch:
           
                    yield {f'Post{self.counter}': jobTitle
                            ,'Company': Company
                            ,'Page':response.css('a.b_next.buildLink').attrib['data-path'][-2:]
                            #'City':job.xpath('//p[1]/text()').get().replace('\r\n','').strip()
                            ,'Date': job.xpath('.//p[3]/text()').get().replace('\r\n','').strip()
                            ,'Enlace':f"{schema}{job.xpath('.//h1/a').attrib['href']}"
                        }
                    
                    self.counter+=1 

            # following page search
                next_page = response.css('a.b_next.buildLink').attrib['data-path']
                if next_page is not None:
                    yield response.follow(next_page, callback=self.parse)

