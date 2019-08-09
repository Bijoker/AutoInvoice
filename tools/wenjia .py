import os
import time

from win32com.client import Dispatch
import win32com.client
import configparser

from tools.msg_Box import msgBox

confpath = r'config.ini'
conf = configparser.ConfigParser()
conf.read(confpath, encoding='utf-8')
notPrintPath = conf['path']['notPrintPath']
notProcessPath = conf['path']['notProcessPath']


def dataHandle(notPrintPath, notProcessPath):
    excel = win32com.client.Dispatch('Excel.Application')
    Visible = excel.Visible = True

    work_book = excel.Workbooks.Open(notPrintPath)
    sheet = work_book.WorkSheets.Item(1).Usedrange

    work_book_1 = excel.Workbooks.Open(notProcessPath)
    sheet_1 = work_book_1.WorkSheets.Item(1).Usedrange
    for row in range(sheet.Rows.Count, 0, -1):
        if sheet.Cells(row, 'W').Value == '已打印':
            value = sheet.Rows(row).Value
            print(value, len(value[0]))
            rows = sheet_1.Rows.Count + 1
            columns = sheet.Columns.Count
            print(rows, columns)
            sheet_1.Range(sheet_1.Cells(rows, 1), sheet_1.Cells(rows, 26)).Value = value
            work_book_1.Save()
            sheet_1 = work_book_1.WorkSheets.Item(1).Usedrange

            sheet.Rows(row).Delete()
            work_book.Save()
            sheet = work_book.WorkSheets.Item(1).Usedrange
            print(sheet.Rows.Count)
    work_book.Close()
    work_book_1.Close()
    excel.Quit()
if __name__ == '__main__':
    try:
        dataHandle(notPrintPath, notProcessPath)
    except Exception as e:
        with open(r'errlog.txt', 'w', encoding='utf-8') as f:
            f.write(time.strftime('%Y%m%d%H%M%S', time.localtime()) + '\n')
            f.write(str(e))
        print(e)
        msgBox(text=e, caption='程序错误')
        exit()
