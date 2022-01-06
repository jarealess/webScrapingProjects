from scrapy import settings
from scrapy.exporters import CsvItemExporter

class MyProjectCsvItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = ';'
        kwargs['delimiter'] = delimiter    
        
        
        super(MyProjectCsvItemExporter, self).__init__(*args, **kwargs) 