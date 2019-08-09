import xlrd
import os

from xls.writeXls import writeListToXls


def removeRowXls(path, row=0, sheetIndex=0):
    if not os.path.exists(path):
        BaseException('文件不存在')
    list2D = []
    workbook = xlrd.open_workbook(path)
    sheet1 = workbook.sheets()[sheetIndex]
    nrows = sheet1.nrows
    for r in range(nrows):
        if r == row:
            continue
        rowList = sheet1.row_values(r)
        list2D.append(rowList)
    os.remove(path)
    writeListToXls(list2D, path)
    return sheet1.row_values(row)




def removeColumXls(path, colum=0, sheetIndex=0):
    if not os.path.exists(path):
        BaseException('文件不存在')
    list2D = []
    workbook = xlrd.open_workbook(path)
    sheet1 = workbook.sheets()[sheetIndex]
    ncolums = sheet1.ncolums
    print(ncolums)
    # for r in range(nrows):
    #     if r == row:
    #         continue
    #     rowList = sheet1.row_values(r)
    #     list2D.append(rowList)
    # os.remove(path)
    # writeListToXls(list2D, path)
    # return sheet1.row_values(row)






# removeColumXls('notPrinted.xls')





# a = removeRowXls('notPrinted.xls')
# print(a)