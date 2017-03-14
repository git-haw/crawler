import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth


def crawler():
    URL = "http://www.haw358.top/blog/"
    # cookies = {'testCookies_1': 'Hello_Python3', 'testCookies_2': 'Hello_Requests'}
    # headers = {'User-Agent': 'alexkh'}
    try:
        r = requests.get(URL, params={}, timeout=1)
        # print(r.cookies['NID'])
        # print(tuple(r.cookies))
        print(r.headers['content-type'])
        print(r.encoding)
        print(r.text)
        # print(r.content)
        r.raise_for_status()    # 如果响应状态码不是 200，就主动抛出异常
    except requests.RequestException as e:
        print(e)
    else:
        result = r.text
        print(type(result), result, sep='\n')
        # print(r.text, '\n{}\n'.format('*' * 79), r.encoding)


def upload():
    url = 'http://127.0.0.1:5000/upload'
    files = {'file': open('/home/lyb/sjzl.mpg', 'rb')}
    # files = {'file': ('report.jpg', open('/home/lyb/sjzl.mpg', 'rb'))}     #显式的设置文件名
    # files = {'file': ('test.txt', b'Hello Requests.')}  # 必需显式的设置文件名

    r = requests.post(url, files=files)
    print(r.text)


def auth():
    r = requests.get('https://httpbin.org/hidden-basic-auth/user/passwd', auth=HTTPBasicAuth('user', 'passwd'))
    # r = requests.get('https://httpbin.org/hidden-basic-auth/user/passwd', auth=('user', 'passwd'))    # 简写
    requests.get("", auth=HTTPDigestAuth('user', 'pass'))
    print(r.json())


def sign():
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, compress',
               'Accept-Language': 'en-us;q=0.5,en;q=0.3',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

    s = requests.Session()
    s.headers.update(headers)
    # s.auth = ('superuser', '123')
    s.get('https://www.kuaipan.cn/account_login.htm')

    _URL = 'http://www.kuaipan.cn/index.php'
    s.post(_URL, params={'ac': 'account', 'op': 'login'},
           data={'username': '****@foxmail.com', 'userpwd': '********', 'isajax': 'yes'})
    r = s.get(_URL, params={'ac': 'zone', 'op': 'taskdetail'})
    print(r.json())
    s.get(_URL, params={'ac': 'common', 'op': 'usersign'})


def proxy():
    proxies = {
        "http": "http://10.10.1.10:3128",
        "http": "http://user:pass@10.10.1.10:3128/",
        "https": "http://10.10.1.10:1080",
    }

    requests.get("http://www.zhidaow.com", proxies=proxies)


def get_status(url):
    r = requests.get(url, allow_redirects=False)
    return r.status_code


def test():
    r = requests.get('http://www.github.com', timeout=1)
    print(r.status_code)


if __name__ == '__main__':
    # crawler()
    # test()
    result = get_status("http://www.haw358.top/blog/")
    print(result)
