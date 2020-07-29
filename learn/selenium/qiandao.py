from selenium import webdriver

driver = webdriver.Chrome()
driver.get("http://qd.njulzh.com/")

inputname=driver.find_element_by_css_selector('#app > div > div > div:nth-child(9) > input')
inputname.send_keys('刘子龙')

inputnum=driver.find_element_by_css_selector('#app > div > div > div.input.el-input.el-input--suffix > input')
inputnum.send_keys('181830128')
