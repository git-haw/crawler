from pymongo import MongoClient
from datetime import datetime
import pymongo
from bson.objectid import ObjectId
from bson.son import SON
import pprint
from bson.code import Code


def get_client():
    client = MongoClient()
    # client = MongoClient("localhost", "27017")
    # client = MongoClient("mongodb://localhost:27017")
    return client


def get_db():
    client = get_client()
    db = client.test
    # db = client['test']
    return db


def find():
    db = MongoClient().test
    # coll = db.restaurants
    # coll = db['restaurants']

    # cursor = db.restaurants.find()
    # cursor = db.restaurants.find({"borough": "Manhattan"})
    # cursor = db.restaurants.find({"address.zipcode": "10075"})
    # cursor = db.restaurants.find({"grades.grade": "B"})
    cursor = db.restaurants.find({"grades.score": {"$gt": 30}})
    # cursor = db.restaurants.find({"grades.score": {"$lt": 10}})
    # cursor = db.restaurants.find({"cuisine": "Italian", "address.zipcode": "10075"})
    # cursor = db.restaurants.find(
    #     {"$or": [{"cuisine": "Italian"}, {"address.zipcode": "10075"}]})
    # cursor = db.restaurants.find().sort([
    #     ("borough", pymongo.ASCENDING),
    #     ("address.zipcode", pymongo.ASCENDING)
    # ])

    # cursor = db.restaurants.find({"name": "Juni"})

    for document in cursor:
        print(document)


def insert():
    # db = MongoClient().test
    # result = db.restaurants.insert_one(
    #     {
    #         "address": {
    #             "street": "2 Avenue",
    #             "zipcode": "10075",
    #             "building": "1480",
    #             "coord": [-73.9557413, 40.7720266]
    #         },
    #         "borough": "Manhattan",
    #         "cuisine": "Italian",
    #         "grades": [
    #             {
    #                 "date": datetime.strptime("2014-10-01", "%Y-%m-%d"),
    #                 "grade": "A",
    #                 "score": 11
    #             },
    #             {
    #                 "date": datetime.strptime("2014-01-16", "%Y-%m-%d"),
    #                 "grade": "B",
    #                 "score": 17
    #             }
    #         ],
    #         "name": "Vella",
    #         "restaurant_id": "41704620"
    #     }
    # )

    db = MongoClient().aggregation_example
    result = db.things.insert_many([{"x": 1, "tags": ["dog", "cat"]},
                                    {"x": 2, "tags": ["cat"]},
                                    {"x": 2, "tags": ["mouse", "cat", "dog"]},
                                    {"x": 3, "tags": []}])

    print(result.inserted_ids)


def update():
    db = MongoClient().test

    result = db.restaurants.update_one(
        {"name": "Juni"},
        {
            "$set": {
                "cuisine": "American (New)"
            },
            "$currentDate": {"lastModified": True}
        }
    )

    result = db.restaurants.update_one(
        {"restaurant_id": "41156888"},
        {"$set": {"address.street": "East 31st Street"}}
    )

    result = db.restaurants.update_many(
        {"address.zipcode": "10016", "cuisine": "Other"},
        {
            "$set": {"cuisine": "Category To Be Determined"},
            "$currentDate": {"lastModified": True}
        }
    )

    result = db.restaurants.replace_one(
        {"restaurant_id": "41704620"},
        {
            "name": "Vella 2",
            "address": {
                "coord": [-73.9557413, 40.7720266],
                "building": "1480",
                "street": "2 Avenue",
                "zipcode": "10075"
            }
        }
    )

    print(result.matched_count)
    print(result.modified_count)


def delete():
    db = MongoClient().test
    result = db.restaurants.delete_many({"borough": "Manhattan"})
    # result = db.restaurants.delete_many({})
    # db.restaurants.drop()
    print(result.deleted_count)


def group():
    # db = MongoClient().test
    #
    # cursor = db.restaurants.aggregate(
    #     [
    #         {"$group": {"_id": "$borough", "count": {"$sum": 1}}}
    #     ]
    # )
    #
    # cursor = db.restaurants.aggregate(
    #     [
    #         {"$match": {"borough": "Queens", "cuisine": "Brazilian"}},
    #         {"$group": {"_id": "$address.zipcode", "count": {"$sum": 1}}}
    #     ]
    # )
    #
    # for document in cursor:
    #     print(document)

    pipeline = [
        {"$unwind": "$tags"},
        {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1), ("_id", -1)])}
    ]

    db = MongoClient().aggregation_example
    pprint.pprint(list(db.things.aggregate(pipeline)))


def index():
    db = MongoClient().test
    # result = db.restaurants.create_index([("cuisine", pymongo.ASCENDING)])

    # result = db.restaurants.create_index([
    #     ("cuisine", pymongo.ASCENDING),
    #     ("address.zipcode", pymongo.DESCENDING)
    # ])

    result = db.profiles.create_index([('user_id', pymongo.ASCENDING)], unique=True)

    index_info = sorted(list(db.profiles.index_information()))

    print(result)
    print(index_info)


# The web framework gets post_id from the URL and passes it as a string
def get(post_id):
    db = MongoClient().test
    # Convert from string to ObjectId:
    document = db.test.find_one({'_id': ObjectId(post_id)})
    for doc in document:
        print(doc)


def map_reduce():
    mapper = Code("""
                   function () {
                     this.tags.forEach(function(z) {
                       emit(z, 1);
                     });
                   }
                   """)

    reducer = Code("""
                    function (key, values) {
                      var total = 0;
                      for (var i = 0; i < values.length; i++) {
                        total += values[i];
                      }
                      return total;
                    }
                    """)

    db = MongoClient().aggregation_example

    # result = db.things.map_reduce(mapper, reducer, "myresults", query={"x": {"$lt": 2}})
    #
    # for doc in result.find():
    #     pprint.pprint(doc)

    # pprint.pprint(db.things.map_reduce(mapper, reducer, "myresults", full_response=True))

    # pprint.pprint(
    #     db.things.map_reduce(
    #         mapper,
    #         reducer,
    #         out=SON([("replace", "results"), ("db", "outdb")]),
    #         full_response=True))

    reducer = Code("""
                    function(obj, prev){
                      prev.count++;
                    }
                    """)

    results = db.things.group(key={"x": 1}, condition={}, initial={"count": 0}, reduce=reducer)

    for doc in results:
        pprint.pprint(doc)


if __name__ == '__main__':
    # find()
    # insert()
    # find()
    # update()
    find()
    # group()
    # index()
    # get("58a7145d47a289526a55eba5")
    # map_reduce()
