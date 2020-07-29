import bs4
import requests
import xlwt

book = xlwt.Workbook(encoding='utf-8', style_compression=0)# 新建表格，指定编码即可
sheet = book.add_sheet(u'豆瓣电影Top250', cell_overwrite_ok=True)# 新建sheet，采取可以覆盖读写的方法
# 添加表头
sheet.write(0, 0, '名称')
sheet.write(0, 1, '图片')
sheet.write(0, 2, '排名')
sheet.write(0, 3, '评分')
sheet.write(0, 4, '作者')
sheet.write(0, 5, '简介')
n=1


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

def getPage(pageN):
    url = 'https://movie.douban.com/top250?start='+ str((pageN-1)*25)+'&filter='
    html=getHtml(url)
    if html==None:
        return
    soup=bs4.BeautifulSoup(html,'lxml')
    save_to_excel(soup)

def save_to_excel(soup):
    list = soup.find(class_="grid_view").find_all('li')
    global n
    for item in list:
        # 获取数据
        item_name = item.find(class_='title').string
        item_img = item.find('a').find('img').get('src')
        item_index = item.find(class_='').string
        item_score = item.find(class_='rating_num').string
        item_author = item.find('p').text.strip()
        item_intr = item.find(class_='inq')
        item_intr= item_intr.string if item_intr else ''
        print('爬取电影：' + item_index + ' | ' + item_name + ' | ' + item_score+' | ')
        # 写入表格
        sheet.write(n, 0, item_name)
        sheet.write(n, 1, item_img)
        sheet.write(n, 2, item_index)
        sheet.write(n, 3, item_score)
        sheet.write(n, 4, item_author)
        sheet.write(n, 5, item_intr)
        n+=1


for i in range(1,11):
    getPage(i)

book.save(u'豆瓣最受欢迎的250部电影.xls')
