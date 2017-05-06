from scrapy import Spider
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor


class TestSpider(Spider):
    name = 'TestSpider'
    allowed_domains = ['w3schools.com']
    start_urls = [
        'https://www.w3schools.com/xml/xpath_intro.asp'
    ]

    def parse(self, response):
        # titles = response.xpath("//*[@class='right_menu_body_item']")
        # titles = response.xpath("/html/body/div/div[@id='right']/div[@id='right_menu_body']/*")
        sel = Selector(response)
        divs = sel.xpath('//a/@href')
        print ('title length: ', len(divs))
        for p in divs:

            print (p.extract())

class cnnSpider(Spider):
    name = 'cnnSpider'
    allowed_domains = ['cnn.com']
    start_urls = [
        'http://www.cnn.com'
    ]

    def parse(self, response):
        sel = Selector(response)
        spans = sel.xpath("//@class='cd__headline-text'")
        for span in spans:
            print(span.extract())

class ZVONSpider(Spider):
    name = 'ZVONSpider'
    allowed_domains = ['zvon.org']
    start_urls = [
        'http://www.zvon.org/comp/r/tut-XPath_1.html#intro'
    ]

    def parse(self, response):
        sel = Selector(response)
        divs = sel.xpath("//@class")
        for div in divs:
            print (div.extract())

        linkextract = LinkExtractor()
        links = linkextract.extract_links(response)
        print (links)
