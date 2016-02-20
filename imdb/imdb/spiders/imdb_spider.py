import scrapy

class ImdbSpider(scrapy.Spider):
    name = "imdb"
    allowed_domains = ["imdb.com/"]
    #start_urls = ["http://www.imdb.com/chart/top/",
    #"http://www.imdb.com/year/",
    #"http://www.imdb.com/genre/"]
    start_urls = ["http://www.imdb.com/year/"]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, "wb") as f:
            f.write(response.body)
