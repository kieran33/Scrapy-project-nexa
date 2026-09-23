import scrapy


class BookItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    star_rating = scrapy.Field()
    in_stock = scrapy.Field()
    thumbnail_url = scrapy.Field()
    detail_url = scrapy.Field()
    upc = scrapy.Field()
    description = scrapy.Field()
    number_available = scrapy.Field()
    category = scrapy.Field()
    image_url = scrapy.Field()