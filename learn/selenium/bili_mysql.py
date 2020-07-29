# 使用说明：
# 依赖：python包：selenium, bs4, pymysql；其他：Chrome驱动，mysql处于已启用状态

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import bs4
from selenium.webdriver.chrome.options import Options
import pymysql

# 浏览器初始化
options = Options()
options.add_argument('--headless')
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
browser = webdriver.Chrome(options=options)
WAIT = WebDriverWait(browser, 10)
browser.set_window_size(1400, 900)
browser.get('https://www.bilibili.com/')

# 数据库初始化
db = pymysql.connect('localhost', 'root', '', 'bili_search')
cmd = db.cursor()

def searchB(src):

    table_name=src.replace(' ','_')
    create_table='create table '+table_name+' ( title char(100), link char(100), des char(100), playtime integer, subtitle integer, time char(10), up char(20))'
    clean_table='delete from '+table_name
    try:
        cmd.execute(create_table)
        cmd.execute(clean_table)
        db.commit()
        print("Info | 成功创建空表："+table_name)
    except Exception:
        print("Info | 创建表失败！可能表格已存在。")


    def search():
        try:
            print("Info | 开始尝试访问b站...")
            input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#nav_searchform > input")))
            submit = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#nav_searchform > div > button')))

            input.send_keys(src)
            submit.click()

            print("Info | 搜索成功，转到新窗口")
            all_h = browser.window_handles
            browser.switch_to.window(all_h[1])
            getPage()

            total = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                               '#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.last > button'))).text
            print('Info | 总页数为' + total)
            return int(total)
        except TimeoutException:
            print('Info | 访问超时，尝试重新访问...')
            return search()

    def getPage():
        WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#all-list > div.flow-loader > div.filter-wrap')))
        html = browser.page_source
        soup = bs4.BeautifulSoup(html, 'lxml')
        save_data_to_mysql(soup)

    def save_data_to_mysql(soup):
        list = soup.find(class_='video-list clearfix').find_all(class_='video-item matrix')
        for item in list:
            item_title = item.find('a').get('title')[:100]
            item_link = item.find('a').get('href')[:100]
            item_des = item.find(class_='des hide').text.strip()[:100]
            item_playtime = item.find(class_='so-icon watch-num').text.strip()
            if item_playtime.endswith('万'):
                item_playtime = float(item_playtime[:-1]) * 1000
            item_playtime = str(item_playtime)
            item_subtitle = item.find(class_='so-icon hide').text.strip()
            if item_subtitle.endswith('万'):
                item_subtitle = float(item_subtitle[:-1]) * 1000
            item_subtitle = str(item_subtitle)
            item_time = item.find(class_='so-icon time').text.strip()[:10]
            item_up = item.find(class_='up-name').text[:20]

            print("Info | 读取 | " + item_title)
            insert='insert into '+table_name+' values("'+item_title+'", "'+item_link+'", "'+item_des+'", '+item_playtime+', '+item_subtitle+', "'+item_time+'", "'+item_up+'")'
            cmd.execute(insert)
        try:
            db.commit()
            print("Info | 本页数据已存入数据库！")
        except:
            db.rollback()
            print('\033[7;31mERROR | 数据存入时出现异常！本页数据可能丢失！\033[0m')

    def next_page(des_page):
        try:
            print('Info | 读取下一页...')
            next_btn = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                              '#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.next > button')))
            next_btn.click()
            WAIT.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                                                         '#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.active > button'),
                                                        str(des_page)))
            getPage()
        except TimeoutException:
            print('Info | 访问超时，尝试刷新中...')
            browser.refresh()
            next_page(des_page)


    total = search()
    for i in range(2, total + 1):
        next_page(i)
    browser.close()
    db.close()
    print('Info | ******************************** over ********************************')

if __name__ == '__main__':
    src = input("Input | 请输入要搜索的内容：")
    searchB(src)