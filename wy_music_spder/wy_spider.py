# -*- coding: utf-8 -*-
from urllib import request
import re

url = 'http://music.163.com/discover/toplist?id=3778678'
html = request.urlopen(url).read().decode('utf-8')
pa = re.compile("<a\shref=..song.id=\d{1,20}..>.+?<.a>")
dataList = pa.findall(html)

num = 1
for data in dataList:
    print(str(num) + "   " + data)
    num += 1
