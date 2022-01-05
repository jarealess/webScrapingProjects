import scrapy

# https://www.youtube.com/watch?v=S_znhijDygM&ab_channel=FrankAndrade

class WorldometerSpider(scrapy.Spider):
    name = 'worldometer'
    allowed_domains = ['www.worldometers.info/']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        rows = response.xpath('//tr')

        for row in rows:
           # title = response.xpath('//h1/text()').get()
            country = row.xpath('./td/a/text()').get()
            population = row.xpath('./td[3]/text()').get()

            yield {
                'country': country,
                'population': population
            }
