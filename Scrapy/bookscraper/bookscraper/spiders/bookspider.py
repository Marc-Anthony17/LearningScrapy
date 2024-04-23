import scrapy
from bookscraper.items import BookItem

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            relativeUrl = book.css('h3 a ::attr(href)').get()
                
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
        book_item = BookItem()
        
        book_item['url'] = response.url,
        book_item['title'] = response.css('.product_main h1::text').get(),
        book_item['upc'] = table_rows[0].css("td ::text").get(),
        book_item['product_type'] = table_rows[1].css("td ::text").get(),
        book_item['price_excl_tax'] = table_rows[2].css("td ::text").get(),
        book_item['price_incl_tax'] = table_rows[3].css("td ::text").get(),
        book_item['tax'] = table_rows[4].css("td ::text").get(),
        book_item['availability'] = table_rows[5].css("td ::text").get(),
        book_item['num_reviews'] = table_rows[6].css("td ::text").get(),
        book_item['stars'] = response.css("p.star-rating").attrib['class'],
        book_item['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(), 
        book_item['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        book_item['price'] = response.css('p.price_color ::text').get(),


            
        yield book_item
        