import scrapy

from imdb.items import ImdbItem

class ImdbSpider(scrapy.Spider):
    name = "imdb"
    allowed_domains = ["imdb.com/"]
    start_urls = ["http://www.imdb.com/year/"]

    def parse(self, response):
        for href in response.xpath('//table[@class="splash"]/tr/td/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_articles_follow_next_page)

    #def parse_by_year(self, response):
    #    for sel in response.xpath('//table[@class="splash"]/tr/td/a/@href'):
    #        item = ImdbItem()
    #        item['year'] = sel.xpath('a/@href').extract()
    #        yield item

    def parse_articles_follow_next_page(self, response):
        #for movie in
        #
        # extract data for each movie
        #
        #yield item
        #
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse_articles_follow_next_page)
