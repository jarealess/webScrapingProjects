import scrapy

# https://www.youtube.com/watch?v=s4jtkzHhLzY&t=1002s&ab_channel=JohnWatsonRooney

class WhiskyspiderSpider(scrapy.Spider):
    name = 'whiskyspider'
   # allowed_domains = ['https://www.whiskyshop.com/scotch-whisky?item_availability=In+Stock']
    start_urls = ['https://www.whiskyshop.com/scotch-whisky?item_availability=In+Stock']

    def parse(self, response):
        products = response.css('div.product-item-info')

        for product in products:
            yield {
                'name': product.css('a.product-item-link::text').get(),
                'price': product.css('span.price::text').get(),
                'link': product.css('a.product-item-link').attrib['href']
            }


        # para navegar a una nueva página (con el botón de next)
        next_page = response.css('a.action.next').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)