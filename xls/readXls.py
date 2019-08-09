import xlrd
import os

def isAcquisition(path,colum,sheetIndex=0):
    """
    :param path: filepath
    :param colum: 列
    :param sheetIndex  defatule = 0
    :return: err  or  list
    """

    if not os.path.exists(path):
        BaseException('文件不存在')
    workbook = xlrd.open_workbook(path)

    sheet1 = workbook.sheets()[sheetIndex]
    cols = sheet1.col_values(colum)
    return cols

def readXlsCell(path,row=0,colum=0,sheetIndex=0):
    if not os.path.exists(path):
        BaseException('文件不存在')
    workbook = xlrd.open_workbook(path)
    sheet1 = workbook.sheets()[sheetIndex]
    value = sheet1.cell(row, colum).value
    return value
