#use requests library
import requests

#import unittest library
import unittest

#use scrapy library
import scrapy

class mySpider(scrapy.Spider):
    url = " http://172.18.58.238/multi"
    r = requests.get(url)
    print(r.text)
    print("Status code:")
    print("\t *", r.status_code)
    h = requests.head(url)
    print("Header:")
    print("**********")
    for x in h.headers:
        print("\t", x, ":", h.headers[x])
    print("**********")
    # This will modify the headers user-agent
    headers = {
        'User-Agent': "Mobile"
    }
    # Test it on an external site
    url2 = 'http://172.18.58.238/headers.php'
    rh = requests.get(url2, headers=headers)
    print(rh.text)

    name = "new_spider"
    start_urls = ['http://172.18.58.238/multi']
    def parse(self, response):
        xpath_selector = '//img'
        for x in response.xpath(xpath_selector):
            newsel = '@src'
            yield {
                'Image Link': x.xpath(newsel).extract_first(),
            }

        Page_selector = '.next a ::attr(href)'
        next_page = response.css(Page_selector).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )

class Test_MySpider(unittest.TestCase):
    def test_spider(self):
        mySpider()
if __name__ == '__main__':
    unittest.main()


