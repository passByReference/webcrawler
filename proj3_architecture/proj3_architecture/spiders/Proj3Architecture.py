from scrapy import Spider
from scrapy.loader import ItemLoader

from proj3_architecture.items import Proj3ArchitectureItem

class Proj3Architecture(Spider):
    name = 'quotes'
    allowed_domains = ['http://quotes.toscrape.com/']
    start_urls = (
        'http://quotes.toscrape.com',
    )

    def parse(self, response):
        l = ItemLoader(item = Proj3ArchitectureItem(), response = response)
        h1_tag = response.xpath('//h1/a/text()').extract_first()
        tags = response.xpath('//*[@class="tag-item"]/a/text()').extract()
        l.add_value('_h1_tag', h1_tag) # _h1_tag corresponds to the variable declared in items.py
        # l.add_value('_tags', tags)
        l.add_xpath('_tags', '//*[@class="tag-item"]/a/text()') # same as l.add_value('_tags', tags)
        return l.load_item()