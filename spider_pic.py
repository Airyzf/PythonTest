import urllib
import urllib.request
import re
import socket
import os
import sys
import requests
import util.dir_util as dirutil

head = 'http://speech.ee.ntu.edu.tw/~tlkagk/'

def download_page(url):
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        data = response.read()
    except:
        return None
    return data


def requests_get(url):
    response = requests.get(url)
    return response.text

# def create_folder(folder_name):
#     name = os.path.join(sys.path[0],folder_name)
#     if not os.path.exists(name):
#         os.mkdir(name)
#     return name
#
# def create_file_name(folder,file_name):
#     name = os.path.join(folder,file_name)
#     return name
#
# courses/MLDS_2017/Lecture/Tensorflow_CNN.pdf  courses/MLDS_2017/Lecture/RNNLM (v3).pdf
# courses/MLDS_2017/Lecture/Special Structure (v6).pdf courses/MLDS_2017/Lecture/EBGAN (v9).pdf
def get_file(html, folder):
    # regx = r'courses/[\S]*[\s]*[\S]*[\s]*[\S]*\.pdf'
    regx = r'http://[\S]*\.jpg'
    pattern = re.compile(regx)
    get_f = re.findall(pattern, repr(html))
    num = 1
    folder = dirutil.DirHelper.create_folder(folder)
    for f in get_f:
        names = f.split(r'/')
        name = '{0}.{1}'.format(num, names[len(names) - 1])
        address = f
        file = download_page(address)
        if file is None:
            num += 1
            continue
        try:
            path = dirutil.DirHelper.create_file_name(folder,name)
            with open(path, 'wb') as fp:
                fp.write(file)
                print('正在下载 ' + name)
                num += 1
                # print('正在下载 ' + name)
        except:
            continue
    return


hzw = 'http://p1.yaojingweiba.com/ckmov/index.php?url=%E6%9C%AA%E7%9F%A5'
url = 'http://speech.ee.ntu.edu.tw/~tlkagk/courses_ML17.html'
new_url = 'http://speech.ee.ntu.edu.tw/~tlkagk/courses_MLDS17.html'
baidu = 'http://huaban.com/favorite/beauty/'
html = download_page(baidu)

get_file(html, 'tmp')
print('下载完成')
