from selenium import webdriver
from bs4 import BeautifulSoup
import time
import undetected_chromedriver as uc
from urllib.parse import urljoin

#get a list of the categories urls
def get_book_urls_by_categories():
    try:
        #Chromedriver to get the webpage html
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = uc.Chrome(options=options)
        url = f"http://books.toscrape.com"
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        #Look side categories panel, and skip the index
        main_ul = soup.find("ul", class_="nav nav-list")
        main_li = main_ul.find("li")
        snd_ul = main_li.find("ul")
        all_links = snd_ul.find_all("a")

        #Get categories links, and retrieve it
        categories_urls = []
        for link in all_links:
            text = link.get_text(strip=True)
            href = link.get("href")
            full_url = urljoin(url, href)
            categories_urls.append({"category": text, "url": full_url})

    finally:
        driver.quit()

    return categories_urls