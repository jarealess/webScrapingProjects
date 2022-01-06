import scrapy


class DrugrecommendscrapeSpider(scrapy.Spider):
    name = 'DrugRecommendScrape'
    #allowed_domains = ['https://medlineplus.gov/spanish/druginfo/drug_Aa.html']
    start_urls = ['https://medlineplus.gov/spanish/druginfo/drug_Aa.html']

    def parse(self, response):
        indice = response.css('ul#index') 
        drugs = indice.xpath('./li')

        for drug in drugs:
            if drug.xpath("./a").attrib["href"] is not None:
                yield {
                    'name': drug.xpath('./a/text()').get(),
                    'link': f'{"https://medlineplus.gov/spanish/druginfo"}{drug.xpath("./a").attrib["href"][1:]}'
                } 
