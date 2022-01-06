import scrapy
from scrapy.linkextractors import LinkExtractor


class getDrugsInfoSpider(scrapy.Spider):
    name = 'getDrugsInfo'

    start_urls = ['https://medlineplus.gov/spanish/druginfo/meds/a601168-es.html']


    # def parse(self, response):
    #    extactor = LinkExtractor(allow_domains = 'medlineplus.gov')
    #    links = extactor.extract_links(response)
    #    for link in links:
    #        print(link.url)
        
    def parse(self, response):
        try:
            texto = {'text': response.xpath('//section/div[contains(@id,"why")]/div[2]/p/text()').get()
            }
        except:
            print('Not description')

        return texto