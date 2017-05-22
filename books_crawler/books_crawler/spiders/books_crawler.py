# -*- coding: utf-8 -*-
import logging
from scrapy import Spider
from scrapy.http import Request


logging.basicConfig(filename='BooksSpider.log',
                    filemode='w',  # logging for each run will start afresh
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s')
logger = logging.getLogger()


def product_info(response, value):
    return response.xpath('//th[text()="' + value + '"]/following-sibling::td/text()').extract_first()


class BookSpider(Spider):
    name = 'BookSpider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']

    def parse(self, response):
        categories = response.xpath('//ul/li/a/@href').extract()
        for category in categories:
            category_url = response.urljoin(category)
            yield Request(category_url, callback=self.parse_category)

    def parse_category(self, response):
        books = response.xpath('//h3/a/@href').extract()
        category = response.xpath('//h1/text()').extract()
        logger.info('Scraping category: {}'.format(category))
        for book in books:
            absolute_url = response.urljoin(book)
            yield Request(absolute_url, callback=self.parse_book)

        # process next page
        next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield Request(absolute_next_page_url, callback=self.parse_category)

    def parse_book(self, response):
        category = response.xpath('//li/a/text()')[-1].extract()
        title = response.css('h1::text').extract_first()
        logger.info('Scraping book: {}'.format(title))
        price = response.xpath('//*[@class="price_color"]/text()').extract_first()

        image_url = response.xpath('//img/@src').extract_first()
        image_url = image_url.replace('../..', 'http://books.toscrape.com/')

        rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
        rating = rating.replace('star-rating ', '')

        description = response.xpath(
            '//*[@id="product_description"]/following-sibling::p/text()').extract_first()

        # product information data points
        upc = product_info(response, 'UPC')
        product_type =  product_info(response, 'Product Type')
        price_without_tax = product_info(response, 'Price (excl. tax)')
        price_with_tax = product_info(response, 'Price (incl. tax)')
        tax = product_info(response, 'Tax')
        availability = product_info(response, 'Availability')
        number_of_reviews = product_info(response, 'Number of reviews')

        yield {
            'category': category,
            'title': title,
            'price': price,
            'image_url': image_url,
            'rating': rating,
            'description': description,
            'upc': upc,
            'product_type': product_type,
            'price_without_tax': price_without_tax,
            'price_with_tax': price_with_tax,
            'tax': tax,
            'availability': availability,
            'number_of_reviews': number_of_reviews
        }