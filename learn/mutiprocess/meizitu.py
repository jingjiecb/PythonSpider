import multiprocessing
import bs4
import requests
import os

# 网上找到的可用headers，可用
header2 = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
    'Connection': 'Keep-Alive',
    'Referer': "http://www.mzitu.com/99566"
}

# 将获取到的随机ip转化成proxies的形式
def get_proxie(ip):
    proxie={
        'http':'http://'+ip
    }
    return proxie

# 获得随机代理ip，注意后台要开proxypool
PROXY_POOL_URL = 'http://localhost:5555/random'
def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return get_proxie(response.text)
    except ConnectionError:
        return None


# 基本请求方法
def request_page(url):
    try:
        # proxie = get_proxy()
        # print(proxie)
        response = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240'})
        if response.status_code == 200:
            return response.text
        print('Status Code Error: '+str(response.status_code))
        return None
    except requests.RequestException:
        print('Link fail!')
        return None

# 获得前n个网页上所有meizi
def get_urls(start,end):
    baseUrl='https://www.mzitu.com/page/'
    res=[]
    for i in range(start,end+1):
        faUrl=baseUrl+str(i)+'/'
        html=request_page(faUrl)
        soup=bs4.BeautifulSoup(html,'lxml')
        list=soup.find(class_='postlist').find_all('li')
        for item in list:
            url=item.find('span').find('a').get('href')
            res.append(url)
    # print(res)
    return res

# 下载一个meizi
def downloadUrl(url):
    html=request_page(url)
    soup=bs4.BeautifulSoup(html,'lxml')
    total=int(soup.find(class_='pagenavi').find_all('a')[-2].string)
    title=soup.find('h2').string
    image_list=[]
    for i in range(total):
        imgHtml=request_page(url+'/'+str(i+1))
        imgSoup=bs4.BeautifulSoup(imgHtml,'lxml')
        imgUrl=imgSoup.find('img').get('src')
        #print(imgUrl)
        image_list.append(imgUrl)
    downloadList(title,image_list)

#下载一个meizi的所有图
def downloadList(title,image_list):
    os.mkdir('ImgDownload/'+title)
    cnt=1
    for img in image_list:
        filename = 'ImgDownload/%s/%s.jpg' % (title, str(cnt))
        print('downloading....%s : NO.%s' % (title, str(cnt)))
        print('from: '+img)
        with open(filename,'wb') as f:
            imgC = requests.get(img,headers=header2).content
            f.write(imgC)
        cnt+=1

# 多线程
if __name__=='__main__':
    meiZis=get_urls(2,2)
    os.mkdir('ImgDownload')
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    pool.map(downloadUrl,meiZis)
    pool.close()
    pool.join()
    print('****************************over****************************')
