from scrapy import Spider, Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from imdb.items import ImdbItem
from scrapy.selector import Selector

class ImdbSpider(CrawlSpider):
    name = "ImdbSpider"
#    allowed_domains = ["www.imdb.com/search/"]
#    start_urls =["http://www.imdb.com/search/title?year={},{}&title_type=feature&sort=moviemeter,asc".format(year, year) for year in range(1920,1930)]
    start_urls = ["http://www.imdb.com/search/title?year=2007,2007&title_type=feature&sort=moviemeter,asc"]
#    custom_settings = {
#            'BOT_NAME': 'imdb-crawler',
#            'DEPTH_LIMIT': 5,
#            'DOWNLOAD_DELAY': 10
#    }
    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="right"]/span/a',)), callback='parse_items', follow=True),
    )

    def parse_items(self, response):
        movies = Selector(response).xpath('//*[@id="main"]/table//tr//td[@class="title"]')
        for movie in movies:
            item = ImdbItem()
            item['title'] = movie.xpath('a/text()').extract()[0]
            item['genres'] = movie.xpath('span[@class="genre"]/a/text()').extract()
            item['year'] = movie.xpath('span[@class="year_type"]/text()').extract()[0][1:-1]
            item['rating'] = movie.xpath('div[@class="user_rating"]/div[@class="rating rating-list"]/span[@class="rating-rating"]/span[@class="value"]/text()').extract()[0]
            try:
                item['runtime'] = movie.xpath('span[@class="runtime"]/text()').extract()[0]
            except:
                item['runtime'] = 9999
            item['imdbID'] = movie.xpath('a/@href').extract()[0][7:-1]
            yield item
