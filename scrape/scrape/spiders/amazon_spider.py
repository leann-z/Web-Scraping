import scrapy
from scrape.items import ScrapeItem

class ProductSpider(scrapy.Spider):
    name = 'amazon_products'
    allowed_domains = ['amazon.com']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
        'DOWNLOAD_DELAY': 3,  
        'COOKIES_ENABLED': True,
        'AUTOTHROTTLE_ENABLED': True,
        'RETRY_TIMES': 10,  
        'RETRY_HTTP_CODES': [503, 500, 502, 403, 404, 400], 
    }

    def start_requests(self):
        urls = [
            'https://www.amazon.com/s?k=smart+watch'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        products = response.css('div.sg-col-inner')
        for product in products:
            #item = ScrapeItem()
            title = product.css('.a-size-medium.a-color-base.a-text-normal::text').get()
            link = product.css('.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal::attr(href)').get()

            if link:
                url = response.urljoin(link)
                yield scrapy.Request(url, callback=self.parse_product, meta={'title': title})

    def parse_product(self, response):
        item = ScrapeItem()
        title = response.meta['title']
        details = response.css('div#feature-bullets ul.a-unordered-list.a-vertical.a-spacing-mini span.a-list-item::text').getall()
        
        if title and details:
            item['title'] = title
            item['details'] = details
            yield item
