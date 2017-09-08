#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: loveNight

import json
import itertools
import urllib
import requests
import os
import re
import sys
import demjson
from bs4 import BeautifulSoup
from util import dir_util

str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}

# str 的translate方法需要用单个字符的十进制unicode编码作为key
# value 中的数字会被当成十进制unicode编码转换成字符
# 也可以直接用字符串作为value
char_table = {ord(key): ord(value) for key, value in char_table.items()}


# 解码图片URL
def decode(url):
    # 先替换字符串
    for key, value in str_table.items():
        url = url.replace(key, value)
    # 再替换剩下的字符
    return url.translate(char_table)


# 生成网址列表，主页的头像
def buildMainPageUrls(page):
    page += 1
    urls = []
    # url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
    url = r'http://www.7799520.com/api/user/pc/list/search?startage=21&endage=27&gender=2&cityid=77&startheight=153&endheight=160&marry=1&page={page}'
    # urls = (url.format(page=x) for x in itertools.count(start=1,step=1))
    for i in range(page):
        if i == 0:
            pass
        else:
            urls.append(url.format(page=i))
    return urls


# 解析JSON获取图片URL
re_url = re.compile(r'"objURL":"(.*?)"')


def resolveImgUrl(html):
    imgUrls = [decode(x) for x in re_url.findall(html)]
    return imgUrls


def downImg(imgUrl, dirpath, imgName):
    filename = os.path.join(dirpath, imgName).replace(':', '')
    try:
        res = requests.get(imgUrl, timeout=15)
        if str(res.status_code)[0] == "4":
            print(str(res.status_code), ":", imgUrl)
            return False
    except Exception as e:
        print(" This is Exception：", imgUrl)
        print(e)
        return False
    try:
        with open(filename, "wb") as f:
            f.write(res.content)
    except Exception as e:
        print(e)
    return True


def download_page(url):
    html = requests.get(url, timeout=10).text  # content.decode('unicode-escape')
    js = json.loads(html)

    # with open("main.html","w") as w:
    #     json.dump(text, w)
    # print(js['data'])

    for item in js['data']['list']:
        # print("username: " + item['username'])
        # print("gender: " + item['gender'])
        # print("city: " + item['city'])
        # print("birthdayyear: " + item['birthdayyear'])
        # print("province: " + item['province'])
        # print("education: " + item['education'])
        # print("height: " + item['height'])
        # print("userid: " + item['userid'])
        # print("monolog: " + item['monolog'])
        # print("avatar: " + item['avatar'])
        imgname = item['username'] + '_' + item['userid'] + '_' + item['birthdayyear'] + '_' + item['height'] + "_"
        # downImg(item['avatar'], "tmp_img", imgname)
        requestPerPage(item['userid'], imgname)
    return html


# 访问详细个人主页
def requestPerPage(id, name):
    turl = r'http://www.7799520.com/user/{id}.html'
    url = turl.format(id=id)
    try:
        content = requests.get(url, timeout=10).content
        print(url)
        soup = BeautifulSoup(content, "lxml")
        lis = soup.find_all("li")
        jpgs = soup.find_all("img")
        count = 1
        exits = []
        tname=name
        for jpg in jpgs:
            if jpg['src'].find("icon") == -1:
                if jpg['src'] not in exits:
                    name = tname + str(count) + '.jpg'
                    downImg(jpg['src'], "tmp_img", name)
                    count += 1
                    exits.append(jpg['src'])
    except:
        print('out time')
        # with open(file_name, "w") as w:
        #     w.write(name + '\r')
        #     for li in lis:
        #         text = li.text
        #         if isContent(text) == 1:
        #             w.write(text.replace('\n', '') + "\r")


def getItems(html):
    reg = re.compile("getData\(")  # 先是要去掉这个头和尾，才会有一个字典的格式，会有key和value
    data = reg.sub(' ', html)
    reg3 = re.compile('\);')
    data = reg3.sub('', data)
    data = json.loads(data)
    for i in data['commentIds']:  # 然后我是用这个for循环来提取出这个data里面的key，然后去掉里面十位数的数字
        pp = re.compile('\d{10}')
        zz = re.findall(pp, i)  # 然后就是用这个数字来当做key来找出value
        # for n in zz:#再用for循环提取出来，赋值给n
        #     try:
        #             w.write(data['comments'][n]['user']['nickname'].encode('utf-8')+'|')#这个就是转一下码
        #             w.write(data['comments'][n]['content'].encode('utf-8')+'|')
        #             w.write(data['comments'][n]['user']['location'].encode('utf-8')+'|')
        #             w.write(data['comments'][n]['createTime'].encode('utf-8')+'|'+'\n')
        #     except:
        #         w.write("null")


def isContent(text):
    flag = 0
    if "现居" in text:
        flag = 1
        text = '\r' + text
    elif "籍贯" in text:
        flag = 1
    elif "星座" in text:
        flag = 1
    elif "生肖" in text:
        flag = 1
    elif "身高" in text:
        flag = 1
    elif "职业" in text:
        flag = 1
    elif "收入" in text:
        flag = 1
    return flag


def test(url):
    html = download_page(url)
    return html


file_name = ''
if __name__ == '__main__':
    floder = dir_util.DirHelper.create_folder("profile")
    file_name = dir_util.DirHelper.create_file_name(floder, "profile.txt")
    urls = buildMainPageUrls(50)
    for url in urls:
        test(url)
        # print(url)
        # with open('main.html', 'r') as f:
        #     json_str = json.load(f)
        #     text = demjson.decode(json_str)
        #     print("")
