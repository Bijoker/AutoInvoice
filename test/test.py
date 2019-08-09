import os
import time

from selenium import webdriver

from xls import writeXls
from chrome.login_Chorme import login
import configparser

from xls.readXls import isAcquisition

timeFlags = time.strftime('%Y%m%d%H%M%S', time.localtime())


confpath = r'config.ini'
conf = configparser.ConfigParser()
conf.read(confpath)


notPrintedFile = conf['baseconfig']['notPrinted']
notProcessedFile = conf['baseconfig']['notProcessed']


user = conf['userconfig']['user']
passwd = conf['userconfig']['password']
urlCertification = conf['url']['urlCertification']
url = conf['url']['urlroot']

driverPath = conf['driver']['driverPath']
# browser = webdriver.Chrome(driverPath)
# browser.get('http://www.baidu.com')
# browser.quit()

print('121343423')
