#-*- codeing = utf-8 -*-
# @Time: 2020-07-20 11:47
# @Author: Claws
# @File: zhihu.py
# @Software: PyCharm
# @Description: zhihu
import requests


def getHtml(url):
    try:
        response=requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'})
        if response.status_code==200:
            return response.text
        else:
            return None
    except requests.RequestException:
        print('Exception!')
        return None

if __name__=="__main__":
    print(getHtml("https://www.zhihu.com/hot"))