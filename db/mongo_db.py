from pymongo import MongoClient


class MongoWorker(object):

    def __init__(self):
        self._client = MongoClient("mongodb://localhost:27017")
        print("connect to mongo, host=%s, port=%d success" % ("127.0.0.1", 27017))

    def insert_one(self, name, value):
        db = self._client.crawl
        db.doc.insert_one(
            {
                "url": name,
                "doc": value
            }
        )
