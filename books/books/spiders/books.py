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
    homepage_url = 'http://books.toscrape.com/'

    def start_requests(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://books.toscrape.com')

        sel = Selector(text=self.driver.page_source)
        print ('chuizi')
        categories = sel.xpath('//ul/li/a/@href').extract()
        print (categories)


        for category in categories:
            print ('category = ', category)
            url = self.homepage_url + category
            self.driver.get(url)
            yield Request(url, callback=self.parse_category)
        return

    def parse_category(self, response):
        books = response.xpath('//h3/a/@href').extract()

        for book in books:
            url = self.homepage_url + book
            self.driver.get(url)
            yield Request(url, callback=self.parse_book)
        while True:
            try:
                # TODO: try using Selector.xpath to get the 'next' url and send it to driver
                next_page = self.driver.find_element_by_xpath('//a[text()="next"]')
                sleep(3)
                self.logger.info('Sleeping for 3 seconds')
                next_page.click()

                sel = Selector(text=self.driver.page_source)
                books = sel.xpath('//h3/a/@href').extract()
                for book in books:
                    url = self.homepage_url + book
                    yield Request(url, callback=self.parse_book)
            except NoSuchElementException:
                self.logger.info('No more pages to load')
                self.driver.quit()
                break

    def parse_book(self, response):
        print ('book url = ', response.url)
