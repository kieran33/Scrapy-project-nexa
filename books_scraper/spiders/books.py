import scrapy

from books_scraper.items import BookItem


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        for book in response.xpath("//article[@class='product_pod']"):
            title = book.xpath(".//h3/a/@title").get()

            price = book.xpath(".//p[@class='price_color']/text()").get()
            price = float(price.replace("£", ""))

            rating = book.xpath(".//p[contains(@class,'star-rating')]/@class").get()
            rating = rating.split(" ")[-1]
            if rating == "One":
                rating = 1
            elif rating == "Two":
                rating = 2
            elif rating == "Three":
                rating = 3
            elif rating == "Four":
                rating = 4
            elif rating == "Five":
                rating = 5

            stock = book.xpath(".//p[contains(@class,'availability')]/text()").getall()
            stock = "".join(stock).strip()
            in_stock = "In stock" in stock

            img = book.xpath(".//img/@src").get()
            img = response.urljoin(img)

            link = book.xpath(".//h3/a/@href").get()

            yield response.follow(link, self.parse_book, cb_kwargs={
                "title": title,
                "price": price,
                "rating": rating,
                "in_stock": in_stock,
                "thumbnail_url": img,
            })

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_book(self, response, title, price, rating, in_stock, thumbnail_url):
        upc = response.xpath("//th[text()='UPC']/following-sibling::td/text()").get()

        desc = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
        if desc is None:
            desc = ""
        desc = desc.strip()
        if desc.endswith("...more"):
            desc = desc[:-7].strip()
        # le site répète parfois la description en entier deux fois
        start = desc.find(desc[:40], 10)
        if start != -1:
            desc = desc[start:]

        avail = response.xpath("//th[text()='Availability']/following-sibling::td/text()").get()
        avail = avail.split("(")[1]
        avail = avail.split(" ")[0]
        number_available = int(avail)

        category = response.xpath("//ul[@class='breadcrumb']/li[3]/a/text()").get()

        image_url = response.xpath("//div[@id='product_gallery']//img/@src").get()
        image_url = response.urljoin(image_url)

        item = BookItem()
        item["title"] = title
        item["price"] = price
        item["star_rating"] = rating
        item["in_stock"] = in_stock
        item["thumbnail_url"] = thumbnail_url
        item["detail_url"] = response.url
        item["upc"] = upc
        item["description"] = desc
        item["number_available"] = number_available
        item["category"] = category
        item["image_url"] = image_url
        yield item