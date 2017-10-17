from scrapy import Request
from scrapy.spiders import Spider

from MongodbConnector import get_collection


class JDProductSpider(Spider):
    name = 'jd-product'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/53.0.2785.143 Safari/537.36',
    }

    def __init__(self):
        self.collection = get_collection("laptop")

    def start_requests(self):
        url_template = 'https://list.jd.com/list.html?cat=670,671,672&page=%d&sort=sort_commentcount_desc&trans=1&JL=4_5_0#J_main'
        for i in range(1042):
            url = url_template % i
            print("=>",url)
            yield Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        body = response.body
        items = response.css('.gl-item')
        i = 0
        for item in items:
            print("======",++i,"===================\n")

            print("===productid", item.css('div::attr(data-sku)').extract())
            productId = item.css('div::attr(data-sku)')[0].extract()
            name = item.css('div>.p-name>a>em::text').extract()[0]
            name = name.strip()
            self.collection.insert({"_id": productId, "name": name})
            print("name", name)

        # yield time()


# spider = JDSpider()
# reqs = spider.start_requests()
# for req in reqs:
#     print("+\n")
