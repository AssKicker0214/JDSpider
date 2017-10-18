import re
import json
from datetime import time

from scrapy import Request
from scrapy.spiders import Spider
from MongodbConnector import AliyunMongo, LocalMongo
import json


class JDCommentSpider(Spider):
    name = 'jd-comment'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/53.0.2785.143 Safari/537.36',
    }

    def __init__(self):
        super()
        # ################# deprecated url###############
        # self.url_template = 'https://club.jd.com/comment/productPageComments.action?' \
        #                     'callback=fetchJSON_comment98vv16416&productId' \
        #                     '=%d&score=0&sortType=5&page=%d&pageSize=10&isShadowSku=0&fold=1'

        # %s的位置是商品id，%d的位置是页数
        self.url_template = 'https://club.jd.com/productpage/p-%s-s-0-t-1-p-%d.html'

        # 构造阿里云数据库连接，将自己名称的简写填入
        self.aliyun = AliyunMongo("qhb")

        # 将爬取的评论保存在本地
        self.local = LocalMongo()

    def start_requests(self):
        # 从阿里云服务器获取任务，get_task可以传入数值参数，代表获取多少个待爬商品
        product_ids = self.aliyun.get_task()
        for product_id in product_ids:
            url = self.url_template % (product_id, 0)
            yield Request(url, headers=self.headers, callback=self.parse, meta={"product-id": product_id, "current-page": 0, "total": 0, "comments": []})

    def parse(self, response):
        page = response.meta["current-page"]
        product_id = response.meta["product-id"]
        total = response.meta["total"]
        comments = response.meta["comments"]
        print("=======parsing product: %s, page: %d========"%(product_id, page))
        content = response.body.decode('gbk')
        commentsRe = re.search(r'(?<="comments":)\[.*\]', content)
        if commentsRe is None or commentsRe.group(0) == '[]':
            print("结束, 提交结果，并存储本地")
            doc = {"_id": product_id, "total_comments": total, "comments": comments}
            self.local.save(doc)
            self.aliyun.commmit_task(product_id, total)
        else:
            raw_comments = commentsRe.group(0)
            raw_comments_json = json.loads(raw_comments)
            for item in raw_comments_json:
                comments.append(
                    dict(id=item["id"], guid=item["guid"], content=item["content"], creationTime=item["creationTime"],
                         referenceId=item["referenceId"], referenceName=item["referenceName"], score=item["score"],
                         usefulVoteCount=item["usefulVoteCount"], uselessVoteCount=item["uselessVoteCount"]))
            subtotal = len(raw_comments_json) + total
            # print(comments_json)
            # print()
            # print(comments_json[0])
            next_page = page + 1
            next_url = self.url_template % (product_id, next_page)
            yield Request(next_url, meta={"product-id": product_id, "current-page": next_page, "total": subtotal, "comments": comments})
# spider = JDSpider()
# reqs = spider.start_requests()
# for req in reqs:
#     print("+\n")
