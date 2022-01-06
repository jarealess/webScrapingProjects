import scrapy
import numpy



class DrugrecommendscrapeSpider(scrapy.Spider):
    name = 'DrugRecommendScrape'
    start_urls = ['https://medlineplus.gov/spanish/druginfo/drug_Aa.html']


    # Para guardar la salida directamente a un CSV
    # También se definió el archivo EXPORTERS y SE LLAMÓ FEED_EXPORTER en SETTINGS
    custom_settings = {
            'FEED_URI': 'DrugsInformation.csv',
            'FEED_FORMAT': 'csv',
            'ROBOTSTXT_OBEY' : True,
            'FEED_EXPORT_ENCODING': 'latin-1'
         }


    ## getting drugs names and links
    def parse(self, response):

        # drugs
        indice = response.css('ul#index') 
        drugs = indice.xpath('./li')
        
        for drug in drugs:
            if drug.xpath("./a").attrib["href"] is not None:
                info_url = f'{"https://medlineplus.gov/spanish/druginfo"}{drug.xpath("./a").attrib["href"][1:]}'
                yield response.follow(info_url, callback=self.parse_sublinks)
        

        # code to navigate thought pages 
        iniciales = response.xpath('//ul[contains(@class, "alpha-links")]/li') #enlaces
        pagination = []
        for letra in iniciales[1:]:
            pagination.append(f'{"https://medlineplus.gov/spanish/druginfo/"}{letra.xpath("./a").attrib["href"]}')

        for page in pagination:
            yield response.follow(page, callback=self.parse)



    # se obtiene información directamente de la página del medicamento 
    def parse_sublinks(self, response):
        yield {
            'Medicamento': response.xpath('//div[contains(@class,"page-title")]/h1/text()').get(),
            'Enlace': response.url,
            'Sintomas' : response.xpath('//section/div[contains(@id,"why")]/div[2]/p/text()').get()
        }
        
  
        
        
