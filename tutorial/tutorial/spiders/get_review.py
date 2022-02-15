import scrapy
# from tutorial.items import ReviewItem
from scrapy_splash import SplashRequest


class ReviewSpider(scrapy.Spider):
    name = 'review'

    def start_requests(self):
        url = 'https://kr.iherb.com/pr/21st-century-calcium-magnesium-zinc-d3-90-tablets/10695'
        product_urls = [
            'https://kr.iherb.com/pr/21st-century-calcium-magnesium-zinc-d3-90-tablets/10695'
        ]
        for url in product_urls:
            yield scrapy.Request(url=url, callback=self.parse_info)

        for i in range(1, 4):
            url = f'https://kr.iherb.com/r/21st-century-calcium-magnesium-zinc-d3-90-tablets/10695?p={i}'
            yield scrapy.Request(url=url, callback=self.parse_review)

    def parse_info(self, response):
        product_name = response.css('div#product-summary-header > h1::text').get().strip()
        upc_code = response.xpath('//*[@id="product-specs-list"]/li[5]/span/text()').get()
        category = response.css('div#breadCrumbs > a::text').getall()
        # item = ReviewItem()
        # item['product_name'] = product_name
        # item['category'] = category
        # item['upc_code'] = upc_code
        print(product_name)
        print(category)
        print(upc_code)

    def parse_review(self, response):
        reviews = response.css('div.review-text::text').getall()
        # item['reviews'] = reviews
        for review in reviews:
            print(review)
