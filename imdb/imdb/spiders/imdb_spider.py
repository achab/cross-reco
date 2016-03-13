from scrapy import Spider, Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from imdb.items import ImdbItem
from scrapy.selector import Selector

class ImdbSpider(CrawlSpider):
    name = "ImdbSpider"
    allowed_domains = ["imdb.com/year/"]
#    start_urls = ["http://www.imdb.com/year/"]
    start_urls =["http://www.imdb.com/search/title?year=1956,1956&title_type=feature&sort=moviemeter,asc"]
    custom_settings = {
            'BOT_NAME': 'imdb-crawler',
            'DEPTH_LIMIT': 5,
            'DOWNLOAD_DELAY': 10
    }
#    rules = (
#        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True)
#    )

    def parse(self, response):
        s = Selector(response)
        #next_link = s.xpath('//*[@id="right"]/span/a/@href').extract()[0]
        #if len(next_link):
        #    self.make_requests_from_url(next_link)
        movies = Selector(response).xpath('//*[@id="main"]/table//tr//td[@class="title"]')
        for movie in movies:
            item = ImdbItem()
            item['title'] = movie.xpath('a/text()').extract()[0]
            item['genres'] = movie.xpath('span[@class="genre"]/a/text()').extract()
            item['year'] = movie.xpath('span[@class="year_type"]/text()').extract()[0][1:-1]
            item['rating'] = movie.xpath('div[@class="user_rating"]/div[@class="rating rating-list"]/span[@class="rating-rating"]/span[@class="value"]/text()').extract()[0]
            item['runtime'] = movie.xpath('span[@class="runtime"]/text()').extract()[0]
            item['imdbID'] = movie.xpath('a/@href').extract()[0][7:-1]
            yield item
