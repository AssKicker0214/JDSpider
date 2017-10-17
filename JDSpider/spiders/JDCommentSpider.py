import re
import json
from datetime import time

from scrapy import Request
from scrapy.spiders import Spider
from MongodbConnector import AliyunMongo
import json


class JDCommentSpider(Spider):
    name = 'jd-comment'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/53.0.2785.143 Safari/537.36',
    }

    def __init__(self):
        super()
        # self.url_template = 'https://club.jd.com/comment/productPageComments.action?' \
        #                     'callback=fetchJSON_comment98vv16416&productId' \
        #                     '=%d&score=0&sortType=5&page=%d&pageSize=10&isShadowSku=0&fold=1'
        self.url_template = 'https://club.jd.com/productpage/p-%s-s-0-t-1-p-%d.html'
        self.aliyun = AliyunMongo("qhb")

    def start_requests(self):
        # product_ids = aliyun.get_task()
        product_ids = ['1973564623']
        for product_id in product_ids:
            url = self.url_template % (product_id, 0)
            print("=>", url)
            yield Request(url, headers=self.headers, callback=self.parse, meta={"product-id": product_id, "current-page": 0, "total": 0})

    def parse(self, response):
        page = response.meta["current-page"]
        product_id = response.meta["product-id"]
        total = response.meta["total"]
        print("===============parsing page", page)
        content = response.body.decode('gbk')
        commentsRe = re.search(r'(?<="comments":)\[.*\]', content)
        if commentsRe is None or commentsRe.group(0) == '[]':
            print("结束, 提交结果，并存储本地")
            self.aliyun.commmit_task(product_id, total)
        else:
            comments = commentsRe.group(0)
            comments_json = json.loads(comments)
            subtotal = len(comments_json) + total
            print(subtotal)
            next_page = page + 1
            next_url = self.url_template % (product_id, next_page)
            yield Request(next_url, meta={"product-id": product_id, "current-page": next_page, "total": subtotal})
# spider = JDSpider()
# reqs = spider.start_requests()
# for req in reqs:
#     print("+\n")
