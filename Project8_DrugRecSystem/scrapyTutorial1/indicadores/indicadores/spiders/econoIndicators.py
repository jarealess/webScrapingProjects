import scrapy
import datetime

# https://www.youtube.com/watch?v=L-9X9dRpJh0&ab_channel=AsperosGeek

class economicIndicators(scrapy.Spider):
    name = 'e_indicators'
    start_urls = [
        'https://www.dane.gov.co/indicadores-economicos' 
        ]  ## se pueden poner varias urls

    custom_settings = {
            'FEED_URI': 'Indicadores_economicos.csv',
            'FEED_FORMAT': 'csv',
            'ROBOTSTXT_OBEY' : True,
            'FEED_EXPORT_ENCODING': 'utf-8'
         }



    def parse(self, response):
        indicators = response.xpath('//section[contains(@class, "article-content clearfix") and @itemprop="articleBody"]//table//h2/strong/text()').getall()
        values = response.xpath('//section[contains(@class, "article-content clearfix") and @itemprop="articleBody"]//table//h1/text()').getall()

        for ind, val in zip(indicators, values):
            info = {
                'indicador':ind,
                'valor': val,
                'fecha': datetime.date.today()
            }

            yield info ## esto me llena el csv con c / elemento







