import json
import requests
import re

def getPage(page):
    url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-' + str(page)
    try:
        response=requests.get(url)
        if response.status_code==200:
            items=parseInfo(response.text)
        else:
            return 0
    except requests.RequestException:
        return 0
    for item in items:
        write_item_to_file(item)
    return 1

def parseInfo(html):
    pattern=re.compile('<li>.*?list_num.*?(\d+).*?<div class="name">.*?title="(.*?)".*?<div class="publisher_info">.*?title="(.*?)".*?<div class="publisher_info"><span>(.*?)</span>.*?target="_blank">(.*?)</a></div>.*?<div class="biaosheng">五星评分：<span>(\d+)次',re.S)
    items=re.findall(pattern,html)
    for item in items:
        yield {
            'range':item[0],
            'name':item[1],
            'author':item[2],
            'time':item[3],
            'publisher':item[4],
            'stars':item[5]
        }

def write_item_to_file(item):
    print('开始写入数据 ====> ' + str(item))
    with open('book.txt', 'a', encoding='UTF-8') as f:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')
        f.close()

cnt=1
state=getPage(cnt)
while cnt<=25 and state==1:
    cnt+=1
    state=getPage(cnt)
