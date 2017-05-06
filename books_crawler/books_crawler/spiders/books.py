# -*- coding: utf-8 -*-
from time import sleep

from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException

class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']

    def start_requests(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://books.toscrape.com')

        sel = Selector(text=self.driver.page_source)
        print 'chuizi'
        books = sel.xpath('//h3/a/@href').extract()

        # yield request to each book on current page
        for book in books:
            url = 'http://books.toscrape.com/' + book
            yield Request(url, callback=self.parse_book)

        # yield request to go to next page
        while True:
            try:
                next_page = self.driver.find_element_by_xpath('//a[text()="next"]')
                sleep(3)
                self.logger.info('Sleeping for 3 seconds')
                next_page.click() # this changed the page_source, so selenium goes to the next page
                # print('page_source = ', len(self.driver.page_source))
                sel = Selector(text=self.driver.page_source)
                books = sel.xpath('//h3/a/@href').extract()
                for book in books:
                    url = 'http://books.toscrape.com/catalogue/' + book
                    yield Request(url, callback=self.parse_book)
            except NoSuchElementException:
                self.logger.info('No more pages to load.')
                self.driver.quit()
                break

    def parse_book(self, response):
        pass
