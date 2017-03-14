import re


def get_links1(data):
    # 利用正则查找所有连接
    link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", data)
    return link_list


def get_links2(html):
    """Return a list of links from html
    """
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)


def get_links3(html):
    link = re.compile(r"(?<=href=[\"\'])https?://\S+(?=[\"\'])")
    _valid = re.compile(r'^https?://[^/]+$|^https?://\S+/[^.]+$|^https?://\S+/\S+[.]html?$')
    urls = link.findall(html)
    index = 0
    for url in urls:
        # http://abc.com/a/b.apk
        if _valid.match(url):
            print(url)
        else:
            print(url)
            del urls[index]
            index -= 1
        index += 1

    return urls


def _test1():
    pattern = re.compile(r"(?<=href=[\"\'])https?://\S+(?=[\"\'])")
    pattern2 = re.compile(r'^https?://[^/]+$|^https?://\S+/[^.]+$|^https?://\S+/\S+[.]html?$')
    # s = '<a href=\'http://abc.com/a/b.html" class="more-trigger">更多</a>'
    s = '<a href="http://downpack.baidu.com/baidunews_AndroidPhone_1014720b.htmhtm" class="more-trigger">更多</a>'
    # s = '<link rel="stylesheet" type="text/css" href="https://gss0.bdstatic.com/static/common.html"/><link rel="stylesheet" type="text/css" href="https://gss0.bdstatic.com/5foIcy0a2gI2n2jgoY3K/static/fisp_static/news/focustop/focustop_11fecbd.css"/></head>'
    # s = ""
    match = pattern.search(s)

    if match:
        # 使用Match获得分组信息
        s = match.group()
        print(s)
        match = pattern2.match(s)
        if match:
            print(match.group())
        else:
            print("pattern2 not matched")
    else:
        print("pattern1 not matched")


def _test2():
    pattern = re.compile(r'https?://\S+[/]\S+[.]\S+')
    s = 'https://gss0.bdstatic.com/5foIcy0a2gI2n2jgoY3K/static/fisp_static/news/focustop/focustop_11fecbd.css'
    match = pattern.match(s)
    print(match)

    if match:
        # 使用Match获得分组信息
        print(match.group())
    else:
        print("not matched")


if __name__ == '__main__':
    """
        http://abc.com
        http://abc.com/
        http://abc.com/a
        http://abc.com/a/
        http://abc.com/a/b.html
        http://abc.com/a/b.apk
        (\S+[^/])|(\S+/\S+.html?)
        #
        javascript:;
        javascript:void(0);
        javascript:void(0)

        #{url}
        http://downpack.baidu.com/baidunews_AndroidPhone_1014720b.apk
        https://gss0.bdstatic.com/5foIcy0a2gI2n2jgoY3K/static/fisp_static/news/focustop/focustop_11fecbd.css
        https://gss0.bdstatic.com/5foIcy0a2gI2n2jgoY3K/static/fisp_static/common/module_static_include/module_static_include_3a982b6.css
        <link rel="stylesheet" type="text/css" href="https://gss0.bdstatic.com/5foIcy0a2gI2n2jgoY3K/static/fisp_static/common/module_static_include/module_static_include_3a982b6.css"/><link rel="stylesheet" type="text/css" href="https://gss0.bdstatic.com/5foIcy0a2gI2n2jgoY3K/static/fisp_static/news/focustop/focustop_11fecbd.css"/></head>
        http://downpack.baidu.com/baidunews_AndroidPhone_1014720b.apk
    """
    _test1()
    # _test2()
