from scrapy import Spider
from scrapy.http import Request

class QuotesSpider(Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = [
        'http://quotes.toscrape.com'
    ]


    def parse(self, response):
        quotes = response.xpath("//*[@class='quote']")
        for quote in quotes:
            text = quote.xpath(".//*[@class='text']/text()").extract()
            author = quote.xpath(".//*[@itemprop='author']/text()").extract()
            tags = quote.xpath(".//*[@class='tag']/text()").extract()
            '''
            print text
            print author
            print tags
            '''
            yield {
                "Text" : text,
                "Author" : author,
                "Tags" : tags
            }

        next_page_url = response.xpath("//*[@class='next']/a/@href").extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)

        yield Request(absolute_next_page_url)


