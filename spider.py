# http://speech.ee.ntu.edu.tw/~tlkagk/
import urllib
import urllib.request
import re

head = 'http://speech.ee.ntu.edu.tw/~tlkagk/'

def download_page(url):
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        data = response.read()
    except:
        return None
    return data

# courses/MLDS_2017/Lecture/Tensorflow_CNN.pdf  courses/MLDS_2017/Lecture/RNNLM (v3).pdf
# courses/MLDS_2017/Lecture/Special Structure (v6).pdf courses/MLDS_2017/Lecture/EBGAN (v9).pdf
def get_file(html):
    # regx = r'courses/[\S]*[\s]*[\S]*[\s]*[\S]*\.pdf'
    regx=r'http://[\S]*\.jpg'
    pattern = re.compile(regx)
    get_f = re.findall(pattern, repr(html))
    num = 1
    for f in get_f:
        names = f.split(r'/')
        name = '{0}.{1}'.format(num, names[len(names) - 1])
        address = head + f
        file = download_page(address)
        if file is None:
            num += 1
            continue
        with open(name, 'wb') as fp:
            fp.write(file)
            print('正在下载 ' + name)
            num += 1
        # print('正在下载 ' + name)
    return

hzw='http://p1.yaojingweiba.com/ckmov/index.php?url=%E6%9C%AA%E7%9F%A5'
url = 'http://speech.ee.ntu.edu.tw/~tlkagk/courses_ML17.html'
new_url='http://speech.ee.ntu.edu.tw/~tlkagk/courses_MLDS17.html'
baidu='http://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gbk&word=%C3%C0%C5%AE%CD%BC%C6%AC&fr=ala&ala=1&alatpl=cover&pos=0&hs=2&xthttps=000000'
html = download_page(baidu)
get_file(html)

print('下载完成')
