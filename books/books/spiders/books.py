# -*- coding: utf-8 -*-
from time import sleep
import logging
from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from selenium.common.exceptions import NoSuchElementException

logging.basicConfig(filename='BooksSpider.log',
                    filemode='w',  # logging for each run will start afresh
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s')
logger = logging.getLogger()

# spider with selenium
class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    homepage_url = 'http://books.toscrape.com/'
    num_books = 0;

    def start_requests(self):
        
        self.driver = webdriver.Chrome()
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.driver.get('http://books.toscrape.com')

        sel = Selector(text=self.driver.page_source)
        categories = sel.xpath('//ul/li/a/@href').extract()
        logger.info(categories)

        # each category is crawled
        for category in categories:
            logger.info ('category = {}'.format(category))
            url = self.homepage_url + category
            self.driver.get(url)
            yield Request(url, callback=self.parse_category)

        logger.info('total books: {}'.format(self.num_books))

    def parse_category(self, response):
        self.logger.info('Parsing new Category')
        books = response.xpath('//h3/a/@href').extract()

        for book in books:
            l = book.split('/')
            logger.debug('book link: {}'.format(l[-2]))
            url = self.homepage_url + 'catalogue/' + l[-2] + '/' + l[-1]
            self.driver.get(url)
            yield Request(url, callback=self.parse_book)
        while True:
            try:
                # TODO: try using Selector.xpath to get the 'next' url and send it to driver
                next_page = self.driver.find_element_by_xpath('//a[text()="next"]')
                sleep(3)
                self.logger.info('Sleeping for 3 seconds')
                next_page.click()
                self.logger.info('Go to next page')

                sel = Selector(text=self.driver.page_source)
                books = sel.xpath('//h3/a/@href').extract()
                for book in books:
                    l = book.split('/')
                    logger.debug('book link: {}'.format(l[-2]))
                    url = self.homepage_url + 'catalogue/' + l[-2] + '/' + l[-1]
                    yield Request(url, callback=self.parse_book)
            except NoSuchElementException:
                self.logger.error('No more pages to load')
                self.driver.quit()
                break

    def parse_book(self, response):
        self.logger.debug('Parsing new book')
        logger.debug ('book url = ', response.url)
        sel = Selector(response)
        title = sel.xpath('//h1/text()').extract()
        price = sel.xpath('//p[@class="price_color"]/text()').extract()  # \xa3 is the pound sign
        instock = sel.xpath('//p[@class="instock availability"]/text()').extract()
        # [u'\n    ', u'\n    \n        In stock (22 available)\n    \n']
        rating = sel.xpath('//p[contains(@class, "star-rating")]').extract()
        # t() [u'<p class="star-rating Three">\n        <i class="icon-star"></i>\n
        #  <i class="icon-star"></i>\n        <i class="icon-star"></i>\n
        #  <i class="icon-star"></i>\n        <i class="icon-star"></i>\n\n
        #  <!-- <small><a href="/catalogue/a-light-in-the-attic_1000/reviews/">\n
        # \n                \n                    0 customer reviews\n
        #  \n        </a></small>\n         -->\xa0\n\n\n<!-- \n
        # <a id="write_review" href="/catalogue/a-light-in-the-attic_1000/reviews/add/#addreview" class="btn btn-success btn-sm">\n
        #  Write a review\n    </a>\n\n --></p>']

        product_description = sel.xpath('//article[@class="product_page"]/p/text()').extract()
        product_information = sel.xpath('//article[@class="product_page"]/table[@class="table table-striped"]').extract()

        logger.debug('title   : {}'.format(title))
        logger.debug('price   : {}'.format(price))
        logger.debug('instock?: {}'.format(instock))
        logger.debug('prd desc: {}'.format(product_description))
        self.num_books += 1
        logger.debug('num_books = {} '.format(self.num_books))

    def spider_closed(self):
        self.driver.close()



