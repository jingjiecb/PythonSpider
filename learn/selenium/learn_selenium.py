from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.taobihu.com/account/login/")

input = driver.find_element_by_css_selector('#aw-login-user-name')
input.send_keys("swalc")

input = driver.find_element_by_css_selector('#aw-login-user-password')
input.send_keys('yN3EkiJRwMkv9Bu')

button = driver.find_element_by_css_selector('#login_submit')
button.click()
