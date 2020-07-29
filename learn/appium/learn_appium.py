# coding=utf-8
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Wechat_Moment():
  def __init__(self):
    desired_caps = {
      'platformName': 'Android',
      'deviceName': '5ENDU19118008335',
      'platformVersion': '10',
      'appPackage': 'com.tencent.mm',
      'appActivity': 'com.tencent.mm.ui.LauncherUI'
    }

    self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    self.wait = WebDriverWait(self.driver, 300)
    print('微信启动...')

  def login(self):
    # 获取到登录按钮后点击
    time.sleep(1)
    login_btn=self.driver.find_element_by_id("com.tencent.mm:id/f7i")
    # login_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/f7i")))
    login_btn.click()
    # 获取使用微信号登录按钮
    change_login_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/d35")))
    change_login_btn.click()
    # 获取输入账号元素并输入
    account = self.wait.until(
      EC.presence_of_element_located((By.XPATH, '//*[@resource-id="com.tencent.mm:id/d2u"]/android.widget.EditText')))
    account.send_keys("lzl_022_3339")
    # 获取密码元素并输入
    password = self.wait.until(
      EC.presence_of_element_located((By.XPATH, '//*[@resource-id="com.tencent.mm:id/d3c"]/android.widget.EditText')))
    password.send_keys("Lzl022196207")
    # 登录
    login = self.wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/d2y")))
    login.click()
    # com.tencent.mm:id/dm3 android:id/button1
    confirm=self.wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/dm3")))
    confirm.click()
    confirm=self.wait.until(EC.element_to_be_clickable((By.ID, "android:id/button1")))
    confirm.click()
    # print("请在手机上完成拼图")
    # time.sleep(3)
    # 点击去掉通讯录提示框
    no_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/dlq")))
    no_btn.click()
    print('登录成功！')

if __name__ == '__main__':
    wc_moment = Wechat_Moment()
    wc_moment.login()