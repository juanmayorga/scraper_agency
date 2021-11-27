import scrapy

# XPath
# links = //a[starts-with(@href, "/home/actualidad/noticias/") and (parent::li)]/@href
# title = //span[@id="sites-page-title"]/text()
# paragraph = //div[@class="sites-layout-tile sites-tile-name-header"]//b[not(@class)]/text()


class SpiderCefaa(scrapy.Spider):
    name = 'cefaa'
    start_urls = ['http://www.cefaa.gob.cl/home/actualidad']
    custom_settings = {
        'FEED_URI': 'cefaa.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        links = response.xpath(
            '//a[starts-with(@href, "/home/actualidad/noticias/") and (parent::li)]/@href').getall()

        for link in links:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(link)})

    def parse_link(self, response, **kwargs):
        link = kwargs['url']
        title = response.xpath('//span[@id="sites-page-title"]/text()').get()
        paragraph = response.xpath(
            '//div[@class="sites-layout-tile sites-tile-name-header"]//b[not(@class)]/text()').get()

        yield{
            'url': link,
            'title': title,
            'body': paragraph
        }
