from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import urllib.parse
import time
from bs4 import BeautifulSoup
import requests

class AmazonScraper:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.setup_driver()

    def setup_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        s = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=s, options=options)

    def scrape(self, search_query):
        encoded_query = urllib.parse.quote(search_query)
        url = f'https://www.amazon.com/s?k={encoded_query}'
        self.driver.get(url)
        time.sleep(2) # wait for page to load

        product_links = [a.get_attribute('href') for a in self.driver.find_elements(By.CSS_SELECTOR, 'a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')]

        product_details_set = set()
        product_details = []
        for link in product_links[:10]:  #10 products only for testing purposes
            details = self.get_product_details(link)
            if details not in product_details_set:
                product_details_set.add(details)
                product_details.append(details)

        self.driver.quit()
        return product_details

    def get_product_details(self, url):
        self.driver.get(url)
        time.sleep(2)  # wait for page to load
        
        # parse page content (using bs)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        details_elements = soup.select('.a-unordered-list.a-vertical.a-spacing-mini')
        details = ' | '.join([elem.get_text(strip=True) for elem in details_elements])
        
        return details if details else "no details found."
    


    def close(self):
        self.driver.quit()
