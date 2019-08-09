import os
import xlwt
import xlrd
from xlutils.copy import copy


def writeListToXls(list2D, filepath):
    '''
    仅支持xls格式
    :param list2D:  需要添加的二维列表
    :param filepath: 文件路径
    :return:
    '''

    if os.path.exists(filepath):
        rows = int(xlrd.open_workbook(filepath).sheets()[0].nrows)
        data = xlrd.open_workbook(filepath)
        ws = copy(data)
        worksheet = ws.get_sheet(0)
        for row in range(len(list2D)):
            for colum in range(len(list2D[row])):
                worksheet.write(rows + row, colum, list2D[row][colum])
        ws.save(filepath)
    else:
        workbook = xlwt.Workbook(encoding='ascii')
        worksheet = workbook.add_sheet('sheet_1')
        for row in range(len(list2D)):
            for colum in range(len(list2D[row])):
                worksheet.write(row, colum, list2D[row][colum])
        workbook.save(filepath)

# writeListToXls(l, r'data.xls')
