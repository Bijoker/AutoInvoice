import os,time
from selenium import webdriver

# user = "201814634"
# passwd = "1qaz@WSX"
# urlCertification = 'http://172.16.2.190:8069/'
# url = "http://172.16.2.190:8069/backlog?moduleKey=Invoice"


def login(browser, urlCertification, url, user, passwd):

    os.popen(r'ExecuteLogin.exe')
    browser.get(urlCertification)
    browser.implicitly_wait(10)
    browser.maximize_window()
    username = browser.find_element_by_id("username")
    username.send_keys(user)
    password = browser.find_element_by_id("password")
    password.send_keys(passwd)
    login = browser.find_element_by_id("btnLogin")
    login.click()

    browser.get(url)
    browser.implicitly_wait(10)
    return browser

# login(urlCertification, url, user, passwd)