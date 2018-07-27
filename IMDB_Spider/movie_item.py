import scrapy

class MovieItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    directors = scrapy.Field()
    writers = scrapy.Field()
    stars = scrapy.Field()
    popularity = scrapy.Field()
    review = scrapy.Field()
    rating = scrapy.Field()
    # movie_review = scrapy.Field()


class MovieReview(scrapy.Item):
    id = scrapy.Field()
    movie_id = scrapy.Field()
    content = scrapy.Field()