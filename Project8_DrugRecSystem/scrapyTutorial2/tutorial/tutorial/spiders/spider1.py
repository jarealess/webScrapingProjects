import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    ## con lo siguiente lo que hacemos es bajarnos el código HTML de las dos páginas

    def start_requests(self):
        urls = ['https://quotes.toscrape.com/page/1/',
                'https://quotes.toscrape.com/page/2/']


        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        page = response.url.split("/")[-2]  ## solo estamos tomando el número de la página
        filename = 'quotes-%s.html'% page

        with open(filename, 'wb') as f:
            f.write(response.body)
        
        self.log('Saved file %s' % filename)