from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)
WAIT = WebDriverWait(browser, 10)

def chTen(src):
    try:
        browser.get('http://fanyi.youdao.com/')
        inputSrc=browser.find_element_by_css_selector('#inputOriginal')
        inputSrc.send_keys(src)
        output=WAIT.until(EC.presence_of_element_located((By.XPATH,"//div[@id='transTarget']//p")))
        res=output.text
        print(res)
        browser.close()
        return res
    except TimeoutException:
        chTen(src)

def chTjp(src):
    try:
        browser.get('http://fanyi.youdao.com/')
        langSelect=WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#langSelect')))
        langSelect.click()
        lang=WAIT.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='fanyi']//li[4]//a[1]")))
        lang.click()
        inputP=browser.find_element_by_css_selector('#inputOriginal')
        inputP.send_keys(src)
        output=WAIT.until(EC.presence_of_element_located((By.XPATH,"//div[@id='transTarget']//p")))
        res=output.text
        print(res)
        browser.close()
        return res
    except TimeoutException:
        chTjp(src)


if __name__=='__main__':
    chTjp('请到官网下载')