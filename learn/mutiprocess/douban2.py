import multiprocessing
import bs4
import requests
import xlwt
import xlrd
import os

book = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 新建表格，指定编码即可
sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)  # 新建sheet，采取可以覆盖读写的方法
# 添加表头
sheet.write(0, 0, '名称')
sheet.write(0, 1, '图片')
sheet.write(0, 2, '排名')
sheet.write(0, 3, '评分')
sheet.write(0, 4, '作者')
sheet.write(0, 5, '简介')

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
    book.save('豆瓣最受欢迎的250部电影'+str(pageN)+'.xls')

def save_to_excel(soup):
    list = soup.find(class_="grid_view").find_all('li')
    for item in list:
        # 获取数据
        item_name = item.find(class_='title').string
        item_img = item.find('a').find('img').get('src')
        item_index = int(item.find(class_='').string)
        item_score = item.find(class_='rating_num').string
        item_author = item.find('p').text.strip()
        item_intr = item.find(class_='inq')
        item_intr= item_intr.string if item_intr else ''
        print('爬取电影：' + str(item_index) + ' | ' + item_name + ' | ' + item_score+' | ')
        # 写入表格
        sheet.write(item_index, 0, item_name)
        sheet.write(item_index, 1, item_img)
        sheet.write(item_index, 2, item_index)
        sheet.write(item_index, 3, item_score)
        sheet.write(item_index, 4, item_author)
        sheet.write(item_index, 5, item_intr)

def union_all():
    for i in range(1,11):
        rb = xlrd.open_workbook('豆瓣最受欢迎的250部电影'+str(i)+'.xls')
        src=rb.sheet_by_index(0)
        for j in range((i-1)*25+1,i*25+1):
            for k in range(6):
                sheet.write(j,k,src.cell_value(j,k))
        os.remove('豆瓣最受欢迎的250部电影'+str(i)+'.xls')
    book.save("豆瓣最受欢迎的250部电影.xls")

if __name__=='__main__':
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    pool.map(getPage,range(1,11))
    pool.close()
    pool.join()
    print('****************************over****************************')

    union_all()
