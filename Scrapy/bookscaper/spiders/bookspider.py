import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            relativeUrl = response.css('h3 a ::attr(href)').get()
                
            if 'catalogue/' in relativeUrl:
                bookUrl = 'https://books.toscrape.com/' + relativeUrl
            else:
               bookUrl = 'https://books.toscrape.com/catalogue/' + relativeUrl
            yield response.follow(bookUrl, callback= self.parse_book_page)
        nextPage = response.css('li.next a ::attr(href)').get()
        if nextPage != None:
            if 'catalogue/' in nextPage:
                nextPageUrl = 'https://books.toscrape.com/' + nextPage
            else:
                nextPageUrl = 'https://books.toscrape.com/catalogue/' + nextPage
            yield response.follow(nextPageUrl, callback= self.parse)
    
    def parse_book_page(self, response):
        table_rows = response.css("table tr")
        yield {
            'url' : response.url,
            'title' : response.css('.product_main h1::text').get(),
            'product_type': table_rows[1].css("td ::text").get(),
            'price_excl_tax': table_rows[2].css("td ::text").get(),
            'price_inck_tax': table_rows[3].css("td ::text").get(),
            'tax': table_rows[4].css("td ::text").get(),
            'availability': table_rows[5].css("td ::text").get(),
            'num_reviews': table_rows[6].css("td ::text").get(),
            'satrs': response.css("p.star-rating").attrib['class'],
            'category': response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(), 
            'description': response.


        }
        pass