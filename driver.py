import os

import time

from MongodbConnector import LocalMongo
from MongodbConnector import AliyunMongo


def clear_status(team_member_name):
    local = LocalMongo()
    aliyun = AliyunMongo(team_member_name)
    fails = aliyun.get_failed_pid()
    for fail_id in fails:
        cnt = local.exist(fail_id)
        print(fail_id, cnt)


# clear_status("qhb")
while True:
    # print("==========%d=============" % x)
    os.system("scrapy crawl jd-comment")

    # 间隔60秒
    time.sleep(60)
