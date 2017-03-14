import redis


# class RedisWorker(object):
#     # to_crawl_url = []
#     # already_crawl_url = []
#
#     def __init__(self):
#         pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
#         self._redis = redis.Redis(connection_pool=pool)
#         print("connect to host=%s, port=%d success" % ("127.0.0.1", 6379))

_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
redis_ = redis.Redis(connection_pool=_pool)
print("connect to redis, host=%s, port=%d success" % ("127.0.0.1", 6379))
