import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from opencsv.opencsv import Csv
from gui.messageBox import MessageBox
from chrome.login_Chorme import login
import configparser
from xls.readXls import isAcquisition, readXlsCell
from xls.removeXls import removeRowXls

timeFlags = time.strftime('%Y%m%d%H%M%S', time.localtime())


confpath = r'config.ini'
conf = configparser.ConfigParser()
conf.read(confpath)


notPrintedFile = conf['baseconfig']['notPrinted']
notProcessedFile = conf['baseconfig']['notProcessed']
processedFile = conf['baseconfig']['processed']


user = conf['userconfig']['user']
passwd = conf['userconfig']['password']
urlCertification = conf['url']['urlCertification']
url = conf['url']['urlroot']


driverPath = conf['driver']['driverPath']
browser = webdriver.Chrome(driverPath)




def inWrite(browser, projectIdList, path, topath):

    '''
    :param browser:
    :param projectIdList:  项目集合唯一标识
    :param path:   待处理文件
    :param topath:  处理完成文件
    :return:
    '''


    #声明一个csv对象，后续用来写入内容
    csv = Csv(topath)



    WebDriverWait(browser, 20, 0.5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'k-pager-nav')))
    maxPageDoc = browser.find_element_by_xpath('//*[@id="backlogGrid"]/div[4]/a[4]')
    maxPage = maxPageDoc.get_attribute("data-page")

    while maxPage == "0":
        maxPageDoc = browser.find_element_by_xpath('//*[@id="backlogGrid"]/div[4]/a[4]')
        maxPage = maxPageDoc.get_attribute("data-page")
        time.sleep(0.5)
    print("共%s页" % maxPage)

    pageTage = None
    for page in range(int(maxPage)):
        '换页标志'
        nextPageTage = browser.find_element_by_xpath('//*[@id="backlogGrid"]/div[4]/span').text
        while nextPageTage == pageTage:
            time.sleep(0.5)
            nextPageTage = browser.find_element_by_xpath('//*[@id="backlogGrid"]/div[4]/span').text
        pageTage = nextPageTage

        projectRoot = browser.find_element_by_xpath('//*[@id="backlogGrid"]/div[3]/table/tbody')
        projectDocs = projectRoot.find_elements_by_xpath('//tr/td/a')
        for num in range(len(projectDocs)):
            print('核对信息%d页%d条' % (page, num))
            'a table'
            dataPageDoc = projectRoot.find_elements_by_xpath('//tr/td/a')[num]

            projectId = dataPageDoc.get_attribute("id")
            projectOverView = dataPageDoc.text
            projectTime = projectRoot.find_elements_by_xpath('//tr/td[6]')[num].text
            projectAuthor = projectDocs[num].find_elements_by_xpath('//td[7]')[num].text


            # 点击进入详情页
            dataPageDoc.click()

            "关闭按钮是否可以点击"
            WebDriverWait(browser, 20, 0.5).until(
                EC.element_to_be_clickable((By.ID, 'Dialog_Invoice_close')))

            closeButton = browser.find_element_by_xpath('//*[@id="Dialog_Invoice_close"]')

            # inId = '发票id'
            inId = projectId + projectOverView

            # inType = '发票类型'
            inType = browser.find_element_by_id('Dialog_Invoice_CodeInvoiceType_Name').text

            # inHeader = "公司名称"
            inHeader = browser.find_element_by_id('Dialog_Invoice_PaymentUnitName').text

            # inContent = '内容'
            inContent = browser.find_element_by_id(
                'Dialog_Invoice_InvoiceDetails_InvoiceDetail_1_TaxableServicesName').text

            # inAmount = '开票金额'
            inAmount = browser.find_element_by_id('Dialog_Invoice_TotalPriceAndTax').text

            # rate = '税率'
            rate = browser.find_element_by_id('Dialog_Invoice_InvoiceDetails_InvoiceDetail_1_TaxRate').text

            # tax = '税额'
            tax = browser.find_element_by_id('Dialog_Invoice_InvoiceDetails_InvoiceDetail_1_TaxAmount').text

            # taxNotAmount = '不含税金额'
            taxNotAmount = browser.find_element_by_id(
                'Dialog_Invoice_InvoiceDetails_InvoiceDetail_1_ExcludingTaxAmount').text

            # taxNumber = '客户单位登记号'
            taxNumber = browser.find_element_by_id('Dialog_Invoice_TaxNumber').text

            # address = '客户地址'
            address = browser.find_element_by_id('Dialog_Invoice_Address').text

            # phone = '客户电话'
            phone = browser.find_element_by_id('Dialog_Invoice_Telephone').text

            # backOpening = '开户行'
            backOpening = browser.find_element_by_id('Dialog_Invoice_BankName').text

            # backAccount = '开户号'
            backAccount = browser.find_element_by_id('Dialog_Invoice_BankAccount').text

            # note = '备注'
            note = browser.find_element_by_id('Dialog_Invoice_Remark').text

            # applicant = '申请人'
            applicant = browser.find_element_by_id('Dialog_Invoice_InvoiceApply_Submitter_Name').text

            # manager = '部门'
            manager = browser.find_element_by_id('Dialog_Invoice_ProjectManagerParner').text

            # inAgency = '开票机构'
            inAgency = browser.find_element_by_id(
                'Dialog_Invoice_InvoiceApply_Project_Business_Letterhead_FullName').text

            inCode = browser.find_element_by_id(
                'Dialog_Invoice_InvoiceApply_Project_Business_Letterhead_FullName').get_attribute("value")

            '''
            projectId
            projectOverView
            projectTime
            projectAuthor
            inId
            inType
            inHeader
            '客户编号'
            inContent
            inAmount
            rate
            tax
            taxNotAmount
            taxNumber
            address
            phone
            backOpening
            backAccount
            note
            applicant
            manager
            inAgency 
            '''

            # print(
            #     projectId + "\n" + projectOverView + "\n" + projectTime + "\n" + projectAuthor + "\n" + inId + "\n" + inType + "\n" + inHeader + "\n" + '客户编号' + '\n' + inContent + "\n" + inAmount + "\n" + rate + "\n" + tax + "\n" + taxNotAmount + "\n" + taxNumber + "\n" + address + "\n" + phone + "\n" + backOpening + "\n" + backAccount + "\n" + note + "\n" + applicant + "\n" + manager + "\n" + inAgency)
            # dataList = [
            #     [projectId, projectOverView, projectTime, projectAuthor, inId, inType, inHeader, '客户编号', inContent,
            #      inAmount, rate, tax, taxNotAmount, taxNumber, address, phone, backOpening, backAccount, note,
            #      applicant, manager, inAgency]]


            #判断项目ID是否 待处理状态
            rowIndex = False
            try:
                #返回待处理列表
                rowIndex = projectIdList.index(projectId)
            except:
                rowIndex = False
            if rowIndex != False:
                InvoiceCode = readXlsCell(path, rowIndex, 24)
                Intime = readXlsCell(path, rowIndex, 25)
                browser.find_element_by_id('Dialog_Invoice_InvoiceCode').send_keys(InvoiceCode)
                browser.find_element_by_id('Dialog_Invoice_InvoiceCode').send_keys(Intime)

                print('通过')


                # 提示框
                box = MessageBox()
                print(box.e)
                if box.e:
                    print('开始操作')
                    # 执行数据操作
                    row = removeRowXls(path, rowIndex)
                    #写入csv  a
                    csv.write(row)
                    print('结束执行')

                    # 点击通过按钮
                    #browser.find_element_by_id('Dialog_Invoice_approved').click()
                else:
                    closeButton.click()
                    continue
            "关闭"
            closeButton.click()

        if page == int(maxPage) - 1:
            browser.quit()
        else:
            '翻页k-loading-mask'
            nextPageButton = browser.find_element_by_xpath('//*[@id="backlogGrid"]/div[4]/a[3]')
            nextPageButton.click()
        browser.close()

def main(browser):
    projectOverView = isAcquisition(notProcessedFile, 0, sheetIndex=0)
    browser = login(browser, urlCertification, url, user, passwd)
    inWrite(browser, projectOverView, notProcessedFile, processedFile)
    browser.quit()
if __name__ == "__main__":
    try:
        main(browser)
    except Exception as e:
        with open(r'log\err\%s.txt' % timeFlags, 'w', encoding='utf-8')as f:
            f.write(str(e))
    # main(browser)



