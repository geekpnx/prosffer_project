import scrapy


class NettoSpider(scrapy.Spider):
    name = "netto"
    start_urls = ['https://www.netto-online.de/lebensmittel/c-N01']

    def parse(self, response):
        # Scraping the product names and prices
        products = response.css('a.product__content')
        images = response.css(
            'a.product__tile__img--link img::attr(data-src)').getall()

        
        images = [img for img in images]

        # Ensure the length of products and images are the same
        if len(products) != len(images):
            self.logger.warning("Mismatch between products and images count")

        # Combine name, price, and image URL
        for product, image in zip(products, images):
            name = product.css('div.product__title::text').get().strip()

            # Extract the integer part of the price
            integer_part = product.css(
                'ins.product__current-price::text').get().strip()

            # Try to extract the fractional part of the price, if it exists
            fractional_part = product.css(
                'span.product__current-price--digits-after-comma::text').get()

            # Check if fractional part exists, if not, only use the integer part
            if fractional_part:
                price = f"{integer_part}{fractional_part.strip()}"
            else:
                price = integer_part

            yield {
                'name': name,
                'price': price,
                'image': image,
            }

        # Find the "next page" link
        next_page = response.css(
            'a.pagination__item__arrow.next-page::attr(href)').get()

        if next_page is not None:
            # Follow the next page link if it exists
            yield response.follow(next_page, self.parse)
