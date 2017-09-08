import requests
import urllib

def get(url):
    return requests.get(url, timeout=10).text

def post(url,postDict):
    # postDict = {
    #     'email': '',
    #     'password': ''
    # }
    postData = urllib.parse.urlencode(postDict).encode()
    response = urllib.request.urlopen(url, postData)
    return response.read().decode('UTF8')

url='http://localhost:9210/api/products/3'
postDict = {
    'Id': '4',
    'Name': 'fish',
    'Category':'Groceries',
    'Price':'12M'
}
print(post(url,postDict))