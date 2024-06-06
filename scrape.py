import requests
from bs4 import BeautifulSoup

class ScrapeEngine:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
            'Accept-Language': 'en-GB,en;q=0.9'
        })

    def fetch_page(self, url, timeout=10):
       try:
        response = self.session.get(url, timeout=timeout)
        
        return BeautifulSoup(response.text, 'lxml')
       except requests.exceptions.RequestException as e:
        print(f"error getting {url}: {e}")
        return None

    def scrape(self, url):
        raise NotImplementedError("amazon_scrape's scrape() should override this")
