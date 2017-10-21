import pymongo
from pymongo import MongoClient


def get_collection(collection_name):
    client = MongoClient("localhost", 27017)
    db = client.jd
    collection = db[collection_name]

    return collection


class LocalMongo:
    def __init__(self):
        self.collection = MongoClient("localhost", 27017).jd["comments_part"]

    def save(self, doc):
        self.collection.save(doc)

    def exist(self, pid):
        return self.collection.find({"_id": pid}).count()


class AliyunMongo:
    def __init__(self, team_member_name):
        self.collection = MongoClient("101.132.40.25", 27072).jingdong["product"]
        self.team_member_name = team_member_name

    def get_task(self, number=5):
        for i in range(number):
            doc = self.collection.find_and_modify(query={"status": "free"},
                                                   update={"$set": {"status": "crawling", "crawler": self.team_member_name}})
            # docs = self.collection.find({})
            print("获取任务:")
            print(doc)
            product_id = doc["_id"]
            yield product_id

    def commit_task(self, id, total):
        self.collection.update({"_id": id}, {"$set": {"status": "completed", "crawler": self.team_member_name, "total": total}})

    def get_failed_pid(self):
        cursor = self.collection.find({"status": "crawling", "crawler": self.team_member_name})
        for doc in cursor:
            pid = doc["_id"]
            yield pid
