# coding=utf-8
from urllib import request
import urllib


def getHtml(url):
    page = urllib.request
    html1 = page.read()
    return html1

if __name__ == '__main__':
    html = getHtml("http://tieba.baidu.com/p/2738151262")
    print(html)
