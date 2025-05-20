import scrapy
import pandas as pd
import os
from scrapper.spiders.etl import book_cleanse
from scrapy import signals

current_dir = os.getcwd()
export_dir = os.path.join(current_dir, "scrapper", "spiders", "exports")
os.makedirs(export_dir, exist_ok=True)
output_path = os.path.join(export_dir, "book_data.csv")

class MySpider(scrapy.Spider):
    name = "book_data"
    custom_settings = {
        "FEEDS": {
            output_path: {
                "format": "csv",
                "overwrite": True
            }
        }
    }

    def read_library(self):
        df = pd.read_excel(os.path.join(export_dir,'library.xlsx'), index_col=None)
        list_of_urls = df['URL'].to_list()
        return list_of_urls

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.urls = self.read_library()

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url, callback=self.parse)

    @classmethod 
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)

        return spider       
    def spider_closed(self, spider):
        book_cleanse()
        print("Process completed successfully")

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