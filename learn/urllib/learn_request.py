# 模拟登陆逼乎
from urllib import request,parse
import ssl

context=ssl._create_unverified_context()
url='https://www.taobihu.com/account/ajax/login_process/'
headers={
    'User-Agent':' Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
dict={
    'return_url':'https://www.taobihu.com/',
    'user_name':'swalc',
    'password':'yN3EkiJRwMkv9Bu',
    '_post_type':'ajax'
}
data=bytes(parse.urlencode(dict),'utf-8')
req=request.Request(url,data=data,headers=headers,method='POST')

responce=request.urlopen(req,context=context)
print(responce.read().decode('utf-8'))
