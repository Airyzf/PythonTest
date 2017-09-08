import urllib
import urllib.request

url = 'https://api-cn.faceplusplus.com/humanbodypp/beta/gesture'
# url='https://api-cn.faceplusplus.com/facepp/v3/detect'
values = {'api_key': 'MEoKo3HvPOkLVSuYuCweMmXDH7-sz_qB', 'api_secret': 'z3fPsoKhxOsnLs4a3YrvbEsattxr8yvb',
          'image_url': 'http://imgsrc.baidu.com/forum/pic/item/6213822bd40735fa4d4c21e49e510fb30f24083e.jpg'}
data = urllib.parse.urlencode(values).encode()
# request = urllib.request.Request(url + '?' + data)
response = urllib.request.urlopen(url,data)
data = response.read()
print(data)
print(data.decode('UTF8'))
