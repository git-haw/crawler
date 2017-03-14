from db.redis_db import redis_
from db.mongo_db import MongoWorker
from util import dom
import requests
import logging

mw = MongoWorker()
log = logging.getLogger("app")

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, compress',
           'Accept-Language': 'en-us;q=0.5,en;q=0.3',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'}


def init():
    fo = open("init_crawl_url.conf", "r")

    for line in fo:
        # print(line)
        line = line.replace('\n', '')
        redis_.lpush("to_crawl_url", line)


def crawl(to_crawl_url):
    try:
        resp = requests.get(to_crawl_url, timeout=2, headers=headers)
        resp.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
    except requests.RequestException as e:
        redis_.sadd("error_crawl_url", to_crawl_url)
        log.exception("RequestException", to_crawl_url, e)
    else:
        redis_.sadd("already_crawl_url", to_crawl_url)

        doc = resp.text
        # print(doc)
        mw.insert_one(repr(to_crawl_url), doc)

        # links = dom.get_links1(doc)
        # links = dom.get_links2(doc)
        links = dom.get_links3(doc)
        for link in links:
            print(link)
            redis_.lpush("to_crawl_url", link)


def pre_crawl():
    to_crawl_url = redis_.rpop("to_crawl_url")
    print("to_crawl_url: %s" % to_crawl_url)
    if to_crawl_url:
        result = redis_.sismember("already_crawl_url", to_crawl_url)
        if 0 == result:
            crawl(to_crawl_url)
        else:
            redis_.sadd("repeat_crawl_url", to_crawl_url)
    else:
        import _setting
        if _setting.TO_CRAWL_URL_INIT_FLAG:
            init()
            pre_crawl()
        else:
            print("exit(0)")
            exit(0)

    pre_crawl()


if __name__ == '__main__':
    init()
    pre_crawl()
