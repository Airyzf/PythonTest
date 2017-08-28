import urllib.request
import http.cookiejar
import re
import gzip
import requests

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
}


def getOpener(head):
    # deal with the Cookies
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener


def getXSRF(data):
    cer = re.compile('name=\"_xsrf\" value=\"(.*)\"', flags=0)
    strlist = cer.findall(data)
    return strlist[0]


def ungzip(data):
    try:  # 尝试解压
        print('准备解压.....')
        data = gzip.decompress(data)
        print('解压完毕!')
    except:
        print('无需解压')
    return data


def getContent(url, opener):
    html = opener.open(test).read()
    return html


url = 'http://aiui.xfyun.cn/jupiter-platform/apps/index'
opener = getOpener(header)
op = opener.open(url)
data = op.read()
email = 'yzf_fs@163.com'
password = ''
postDict = {
    'email': email,
    'password': password,
    'rememberme': 'true',
    'captcha_type': 'cn'
}

postData = urllib.parse.urlencode(postDict).encode()
op = opener.open(url, postData)
# data = op.read()

test = 'http://aiui.xfyun.cn/jupiter-platform/taste/getAnswer?appid=all&text=%25e6%2588%2591%25e6%2583%25b3%25e5%2590%25ac%25e6%2588%2590%25e9%2583%25bd&uid=6awzmk'
html = getContent(test, opener)
print(html.decode('utf-8'))
