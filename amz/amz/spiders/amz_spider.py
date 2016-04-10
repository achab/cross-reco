from scrapy import Spider, Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from amz.items import AmzItem
from scrapy.selector import Selector

class AmzSpider(CrawlSpider):
    name = "AmzSpider"
    start_urls = ["https://www.amazon.fr/s/ref=sr_abn_pp_ss_301061?ie=UTF8&bbn=301061&rh=n%3A301061%2Cp_36%3A389154011",
                  "https://www.amazon.fr/s/ref=sr_abn_pp_ss_301061?ie=UTF8&bbn=301061&rh=n%3A301061%2Cp_36%3A389155011",
                  "https://www.amazon.fr/s/ref=sr_abn_pp_ss_301061?ie=UTF8&bbn=301061&rh=n%3A301061%2Cp_36%3A389157011",
                  "https://www.amazon.fr/s/ref=sr_abn_pp_ss_301061?ie=UTF8&bbn=301061&rh=n%3A301061%2Cp_36%3A389160011",
                  "https://www.amazon.fr/s/ref=sr_abn_pp_ss_301061?ie=UTF8&bbn=301061&rh=n%3A301061%2Cp_36%3A389161011"]
#    custom_settings = {
#            'BOT_NAME': 'amz-crawler',
#            'DEPTH_LIMIT': 5,
#            'DOWNLOAD_DELAY': 10
#    }
    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="pagnNextLink"]',)), callback='parse_items', follow=True),
    )

    def parse_items(self, response):
        books = Selector(response).xpath('//*[@id="s-results-list-atf"]')
        for book in books:
            item = AmzItem()
            try:
                item['title'] = item.xpath('a[@class="title"]').extract()[0]
            except:
                item['title'] = 9999
            try:
                item['genres'] = movie.xpath('span[@class="genre"]/a/text()').extract()
            except:
                item['genres'] = 9999
            try:
                item['year'] = movie.xpath('span[@class="year_type"]/text()').extract()[0][1:-1]
            except:
                item['year'] = 9999
            try:
                item['rating'] = movie.xpath('div[@class="user_rating"]/div[@class="rating rating-list"]/span[@class="rating-rating"]/span[@class="value"]/text()').extract()[0]
            except:
                item['rating'] = 9999
            try:
                item['runtime'] = movie.xpath('span[@class="runtime"]/text()').extract()[0]
            except:
                item['runtime'] = 9999
            item['imdbID'] = movie.xpath('a/@href').extract()[0][7:-1]
            yield item
