import scrapy
import pandas as pd
import os
from scrapy import signals
from scrapper.spiders.paths import absolute_paths
from scrapper.spiders.handle_failure import handle_failure_function


export_dir = absolute_paths()

#Define class
class BoosSpider(scrapy.Spider):
    name = "book_data"
    output_path = os.path.join(export_dir, "book_data.csv")
    custom_settings = {
        "FEEDS": {
            output_path: {
                "format": "csv",
                "overwrite": True,
                'DOWNLOAD_DELAY': 1
            }
        }
    }

    #Read the library file to obtain all the ulrs to obtain information of everybook
    def read_library(self):
        df = pd.read_csv(os.path.join(export_dir,'library.csv'), index_col=None)
        list_of_urls = df['URL'].to_list()
        return list_of_urls

    #execute on start
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.urls = self.read_library()
        open(os.path.join(export_dir,"failed_urls_book.txt"), "w").close()

    #Start creating request for every url
    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url,
                                 callback=self.parse,
                                 errback=self.handle_failure,)
        

    @classmethod #to bound the class with the function
    #instantiate objects
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)

        return spider       
    
    #After  completing the process it will run this part of the code
    def spider_closed(self, spider):
        print("Process completed successfully")


    def handle_failure(self, failure):
        handle_failure_function(self, failure, "book")
    
    #parse the data
    def parse(self, response):
        title = response.css("div.product_main > h1::text").get()
        upc = response.xpath("//table[contains(@class,'table-striped')]//tr[th/text()='UPC']/td/text()").get()
        product_type = response.xpath("//table[contains(@class,'table-striped')]//tr[th/text()='Product Type']/td/text()").get()
        price_no_tax = response.xpath("//table[contains(@class,'table-striped')]//tr[th/text()='Price (excl. tax)']/td/text()").get()
        price_tax = response.xpath("//table[contains(@class,'table-striped')]//tr[th/text()='Price (incl. tax)']/td/text()").get()
        tax = response.xpath("//table[contains(@class,'table-striped')]//tr[th/text()='Tax']/td/text()").get()
        stock_quantity = response.xpath("//table[contains(@class,'table-striped')]//tr[th/text()='Availability']/td/text()").get()
        reviews = response.xpath("//table[contains(@class,'table-striped')]//tr[th/text()='Number of reviews']/td/text()").get()

        yield {
            "UPC": upc,
            "Title": title,
            "Product_Type": product_type,
            "Price_No_Tax": price_no_tax,
            "Price_Tax": price_tax,
            "Tax": tax,
            "Stock_quantity": stock_quantity,
            "ReviewQty": reviews,
        }
