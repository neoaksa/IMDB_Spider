import scrapy
from IMDB_Spider.movie_item import MovieItem, MovieReview,MovieStar

class MovieSpider(scrapy.Spider):
    name = 'imdbspider'
    allowed_domains = ['imdb.com']
    start_urls = ['http://www.imdb.com/chart/top',]

    def parse(self,response):
        # retrieve all links for top 250 movies
        links = response.xpath('//tbody[@class="lister-list"]/tr/td[@class="titleColumn"]/a/@href').extract()
        i = 1
        for link in links:
            # generate absolute url for each movie
            abs_url = response.urljoin(link)
            url_next = '//tbody[@class="lister-list"]/tr['+str(i)+']/td[3]/strong/text()'
            rating = response.xpath(url_next).extract()
            if(i <= len(links)):
                i += 1
                yield scrapy.Request(abs_url,callback=self.parse_indetail,meta={'rating':rating,'id':i})

    def parse_indetail(self, response):
        item = MovieItem()
        item['id'] = response.meta['id']
        item['title'] = response.xpath('//div[@class="title_wrapper"]/h1/text()').extract()[0][:-1]
        item['directors'] = response.xpath('//div[@class="credit_summary_item"]/span[@itemprop="director"]/a/span/text()').extract()[0]
        item['writers'] = response.xpath('//div[@class="credit_summary_item"]/span[@itemprop="creator"]/a/span/text()').extract()
        item['stars'] = response.xpath('//div[@class="credit_summary_item"]/span[@itemprop="actors"]/a/span/text()').extract()
        item['popularity'] = response.xpath('//div[@class="titleReviewBarItem"]/a/div/span/text()').extract()
        item['rating'] = response.meta['rating']
        # retrieve all stars information
        star_links = response.xpath('//div[@class="credit_summary_item"]/span[@itemprop="actors"]/a/@href').extract()
        for star_link in star_links:
            abs_url = response.urljoin(star_link)
            star_id = star_link.split('/')[2]
            yield scrapy.Request(abs_url,callback=self.parse_star,meta={'star_id':star_id})
        # retrieve all reviews for each movie
        review_link = response.xpath('//div[@class="user-comments"]/a[2]/@href').extract_first()
        abs_url = response.urljoin(review_link)
        yield scrapy.Request(abs_url,callback=self.parse_review,meta={'movie_id':item['id']})
        yield item

    def parse_review(self, response):
        reviewItem = MovieReview()
        reviewItem['movie_id'] = response.meta['movie_id']
        links = response.xpath('//div[@class="lister-list"]/div/div[1]/div[1]/div[@class="content"]/div[1]/text()').extract()
        i = 1
        while i <= len(links):
            reviewItem['id'] = response.xpath('//div[@class="lister-list"]/div['+str(i)+']/@data-review-id').extract()
            url_next = '//div[@class="lister-list"]/div['+str(i)+']/div[1]/div[1]/div[@class="content"]/div[1]/text()'
            if reviewItem['id']:
                reviewItem['content'] = response.xpath(url_next).extract()
            i += 1
            yield reviewItem

    def parse_star(self,response):
        starItem = MovieStar()
        starItem['name'] = response.xpath('//table[@id="name-overview-widget-layout"]/tbody/tr/td[@id="overview-top"]/h1/span[@class="itemprop"]/text()').extract()
        starItem['id'] = response.meta['star_id']
        starItem['born_year'] = response.xpath('//div[@id="name-born-info"]/time/@datetime').extract()
        starItem['born_area'] = response.xpath('//div[@id="name-born-info"]/a/text()').extract()
        return starItem
