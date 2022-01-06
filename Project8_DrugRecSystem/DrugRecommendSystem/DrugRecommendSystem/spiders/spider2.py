import scrapy
from scrapy.linkextractors import LinkExtractor


class getDrugsInfoSpider(scrapy.Spider):
    name = 'getDrugsInfo'

    start_urls = ['https://medlineplus.gov/spanish/druginfo/drug_Aa.html']


    # def parse(self, response):
    #    extactor = LinkExtractor(allow_domains = 'medlineplus.gov')
    #    links = extactor.extract_links(response)
    #    for link in links:
    #        print(link.url)
        
    def parse(self, response):
        iniciales = response.xpath('//ul[contains(@class, "alpha-links")]/li')

        pagination = []
        for letra in iniciales[1:]:
            pagination.append(f'{"https://medlineplus.gov/spanish/druginfo/"}{letra.xpath("./a").attrib["href"]}')
            
        yield {
            
            'link': pagination
        }