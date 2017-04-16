import scrapy

class AuthorSpider(scrapy.Spider):
    name = 'authors'

    def start_request(self):
        start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
