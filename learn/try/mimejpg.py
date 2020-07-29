#-*- codeing = utf-8 -*-
# @Time: 2020-05-23 8:41
# @Author: Claws
# @File: mimejpg.py
# @Software: PyCharm
# @Description: None
import requests

img='http://localhost:8888/css.jpg'

imgC = requests.get(img)

try:
    with open('css.jpg', 'wb') as f:
        imgC = requests.get(img).content
        f.write(imgC)
except Exception:
    pass