import scrapy
from urllib.parse import urljoin
import time
from scrapper.spiders.categories import get_book_urls_by_categories
from scrapy import signals
from scrapy.exceptions import CloseSpider
import os


#Obtain absolute paths to work in any location
current_dir = os.getcwd()
export_dir = os.path.join(current_dir, "scrapper", "spiders", "exports")
os.makedirs(export_dir, exist_ok=True)
output_path = os.path.join(export_dir, "library.csv")


class MySpider(scrapy.Spider):
    name = "library_data"

    custom_settings = {
        "FEEDS": {
            output_path: {
                "format": "csv",
                "overwrite": True,
                "encoding": "utf-8"
            }
        }
    }

    #execute on start
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 1
        self.dictionary_categories = get_book_urls_by_categories()
        self.category = self.dictionary_categories

    @classmethod #to bound the class with the function
    #instantiate objects
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.handle_spider_error, signal=signals.spider_error)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider
        
    #error handling
    def handle_spider_error(self, failure, response, spider):
        self.logger.error(f"Critical spider error: {failure}")
        raise CloseSpider("Fatal error during crawling/writing. Shutting down.")
    
    #Start creating request for every category url
    def start_requests(self):
        for row in self.dictionary_categories:
            yield scrapy.Request(row["url"], callback=self.parse, meta={"category": row["category"]})

    def handle_failure(self, failure):
        self.logger.warning(f"Request failed or timed out: {failure.request.url} - Reason: {failure.value}")

    #After  completing the process it will run this part of the code
    def spider_closed(self, spider):
        print("Process completed successfully")

    def errback_httpbin(self, failure):
        self.logger.error(f"Failed: {failure.request.url}")
        with open("failed_urls.txt", "a") as f:
            f.write(failure.request.url + "\n")

    #parse the data
    def parse(self, response):
        if not response.body or response.status != 200:
            self.logger.warning(f"Skipping empty or failed response: {response.url}")
            return
        #Map for rating starts
        rating_map = {"One": 1,"Two": 2,"Three": 3,"Four": 4,"Five": 5}
        category = response.meta.get("category", "Unknown")
        #Loop for every book, to obtain values
        for product in response.css("article.product_pod"):
            title = product.css("h3 a::attr(title)").get()
            price = product.css(".price_color::text").get()
            availability_list = product.css("p.instock.availability::text").getall()
            availability = ''.join(availability_list).strip()
            rating_class = product.css("p.star-rating::attr(class)").get()
            rating = None
            #Change rating string for a number
            if rating_class:
                rating_word = rating_class.split()[-1]
                rating = rating_map.get(rating_word)

            relative_url = product.css("h3 a::attr(href)").get()
            full_url = urljoin(response.url, relative_url)
            
            #
            yield {
                "ID": self.counter,
                "Category": category,
                "Title": title,
                "Price": price,
                "Rating": rating,
                "Stock_availability": availability,
                "URL": full_url,
            }

            self.counter += 1
        #if there is a next page to run again in the next url for the same category
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            next_url = urljoin(response.url, next_page)
            yield response.follow(
                next_url,
                callback=self.parse,
                errback=self.errback_httpbin,
                errback=self.handle_failure,
                meta={"category": category, "download_timeout": 10}
            )

    

