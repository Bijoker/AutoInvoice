import time
from win32com.client import Dispatch
import win32com.client


class Excel_Sheet():
    def __init__(self, path, sheetIndex=1):
        self.sheetIndex = sheetIndex
        self.excel = win32com.client.Dispatch('Excel.Application')
        self.Visible = self.excel.Visible = -1
        self.work_book = self.excel.Workbooks.Open(path)
        self.sheet = self.work_book.WorkSheets.Item(self.sheetIndex).Usedrange
        self.shape = (self.sheet.Rows.Count, self.sheet.Columns.Count)
        print('''
        **************************************************************************
        注意，该索引范围为已使用单元格范围，对添加第一行或者添加第一列操作无效
        **************************************************************************
        ''')
    def reloadSheet(self):
        self.work_book.Save()
        self.sheet = self.work_book.WorkSheets.Item(self.sheetIndex).Usedrange


    def addCell(self, rowIndex, columnsIndex, value, shift='right'):
        '''
        https://docs.microsoft.com/zh-cn/office/vba/api/excel.xlinsertshiftdirection
         -4161  向右移动单元格   xlShiftToRight
         -4121  向下移动单元格  xlShiftDown
        :param rowIndex:
        :param columnsIndex:
        :param value:
        :param shift:
        :return:
        '''
        if shift == 'right':
            shift = -4161
        elif shift == 'down':
            shift = -4121
        else:
            return Exception('参数错误')
        self.getCell(rowIndex, columnsIndex).Insert(shift)
        self.sheet = self.work_book.WorkSheets.Item(self.sheetIndex).Usedrange
        self.setCellValue(rowIndex, columnsIndex, value)
        self.reloadSheet()

    def delCell(self,rowIndex, columnsIndex, shift='lift'):
        '''
        https://docs.microsoft.com/zh-cn/office/vba/api/excel.xldeleteshiftdirection
        -4159: 单元格向左移动      xlShiftToLeft
        -4162: 单元格向上移动      xlShiftUp
        :param rowIndex:
        :param columnsIndex:
        :param shift:
        :return:
        '''
        if shift == 'lift':
            shift = -4159
        elif shift == 'up':
            shift = -4162
        else:
            return Exception('参数错误')
        self.getCell(rowIndex, columnsIndex).Delete(shift)
        self.save()
        self.reloadSheet()

    def setCellValue(self, rowIndex, columnsIndex, value):
        self.getCell(rowIndex, columnsIndex).Value = value
        self.save()
        self.reloadSheet()

    def getCell(self, rowIndex, columnsIndex):
        '''
        :type   args int
        :param rowIndex:     行索引  从1开始
        :param columnsIndex: 列索引  从1开始
        :return:
        '''
        return self.sheet.Cells(rowIndex, columnsIndex)
    def getCellValue(self, rowIndex, columnsIndex):
        return self.getCell(rowIndex,columnsIndex).Value



    def insertBlankLine(self,row):
        self.getRow(row).Insert()
        self.save()
        self.reloadSheet()

    def addRow(self, row, value):
        self.insertBlankLine(row)
        self.setRowValue(row, value)
        self.save()
        self.reloadSheet()

    def appendRow(self, value):
        self.addRow(self.shape[0] + 1, value)
        self.save()

    def delRow(self, row):
        self.getRow(row).Delete()
        self.save()
        self.reloadSheet()

    def setRowValue(self,row, value):
        startColumn = self.getCell(row, 1)
        endColumn = self.getCell(row, self.shape[1])
        print(self.sheet.Range(startColumn, endColumn).Value)
        # self.sheet.Range(startColumn, endColumn).Value = value
        self.save()

    def getRow(self, row):
        '''
        获取一行可以使用 int类型或者str类型
        获取多行使用 str类型
        :param rows:  1 or '1'
        :return:
        '''
        return self.sheet.Rows(row)
    def getRowValues(self, row):
        return self.getRow(row).Value



    def addColumn(self, column, value):
        self.getColumn(column).Insert()
        self.setColumnValue(column, value)

    def delColumn(self, column):
        self.getColumn(column).Delete()
        self.save()

    def setColumnValue(self, column, value):
        startRow = self.getCell(1, column)
        endRow = self.getCell(self.shape[0], column)
        self.sheet.Range(startRow, endRow).Value = value
        self.save()

    def getColumn(self,column):
        '''
        获取一列可以使用 int类型或者str类型
        获取多列使用 str类型
        :param columns:  1 or 'A'
        :return:
        '''
        return self.sheet.Columns(column)
    def getColumnValues(self,column):
        return self.getColumn(column).Value




    def addRange(self,rowIndexStart, columnsIndexStart, rowIndexEnd, columnsIndexEnd, values, shift='right'):
        '''
        https://docs.microsoft.com/zh-cn/office/vba/api/excel.xlinsertshiftdirection
         -4161  向右移动单元格   xlShiftToRight
         -4121  向下移动单元格  xlShiftDown
        :param rowIndexStart:
        :param columnsIndexStart:
        :param rowIndexEnd:
        :param columnsIndexEnd:
        :param shift:
        :return:
        '''
        if shift == 'right':
            shift = -4161
        elif shift == 'down':
            shift = -4121
        else:
            return Exception('参数错误')
        startCell = self.getCell(rowIndexStart, columnsIndexStart)
        endCell = self.getCell(rowIndexEnd, columnsIndexEnd)
        self.sheet.Range(startCell, endCell).Insert(shift)
        self.setRangeValue(rowIndexStart, columnsIndexStart, rowIndexEnd, columnsIndexEnd, values)
        self.save()

    def delRange(self,rowIndexStart, columnsIndexStart, rowIndexEnd, columnsIndexEnd, shift='left'):
        '''
        https://docs.microsoft.com/zh-cn/office/vba/api/excel.xldeleteshiftdirection
        -4159: 单元格向左移动      xlShiftToLeft
        -4162: 单元格向上移动      xlShiftUp
        :param rowIndexStart:
        :param columnsIndexStart:
        :param rowIndexEnd:
        :param columnsIndexEnd:
        :param shift:
        :return:
        '''
        if shift == 'lift':
            shift = -4159
        elif shift == 'up':
            shift = -4162
        else:
            return Exception('参数错误')
        startCell = self.getCell(rowIndexStart, columnsIndexStart)
        endCell = self.getCell(rowIndexEnd, columnsIndexEnd)
        self.sheet.Range(startCell, endCell).Delete()
        self.save()

    def setRangeValue(self, rowIndexStart, columnsIndexStart, rowIndexEnd, columnsIndexEnd, values):
        startCell = self.getCell(rowIndexStart, columnsIndexStart)
        endCell = self.getCell(rowIndexEnd, columnsIndexEnd)
        self.sheet.Range(startCell, endCell).Value = values
        self.save()

    def getRange(self,rowIndexStart, columnsIndexStart, rowIndexEnd, columnsIndexEnd):
        return self.sheet.Range(self.getCell(rowIndexStart, columnsIndexStart), self.getCell(rowIndexEnd, columnsIndexEnd))
    def getRangeValue(self,rowIndexStart, columnsIndexStart, rowIndexEnd, columnsIndexEnd):
        return self.getRange(rowIndexStart, columnsIndexStart, rowIndexEnd, columnsIndexEnd).Value


    def getUseRange(self):
        self.rows = self.sheet.Rows.Count
        self.columns = self.sheet.Columns.Count
        rangeFirstCell= self.sheet.Cells(1, 1)
        rangeLastCell = self.sheet.Cells(self.rows, self.columns)
        return self.sheet.Range(rangeFirstCell, rangeLastCell)
    def getUseRangeValue(self):
        return self.getUseRange().Value








    def save(self):
        self.work_book.Save()
    def close(self):
        self.work_book.Close()
    def quit(self):
        self.excel.Quit()
    #
    # def __del__(self):
    #     self.work_book.save
    #     self.work_book.close
    #     self.excel.Quit()



if __name__ == '__main__':
    # Sheet1 = Excel_Sheet(r'D:\Desktop\tzcpa\BJinvoice\invioceveify\notProcessed.xls')
    Sheet2 = Excel_Sheet(r'D:\Desktop\tzcpa\BJinvoice\invioceveify\notProcessed1.xls')
    row = Sheet2.getRow(2)
    print(row.Value)
    # row.Value = (('1', '1', '2018/3/29 11:23:26', '马玉', 'e06d5ebb-9b16-46aa-9462-a8ac00fbd36e', '增值税专用发票', '沈阳广盛鑫源商业投资管理有限公司', None, '咨询费', '600,000.00', '6.00%', '33,962.26', '566,037.74', '912101025507728654', '沈阳市和平区文萃路9号', '024-31077066', '盛京银行沈阳市科技支行', '0317010140940004025', None, '马玉', '瞿艺', '天职（北京）国际工程项目管理有限公司 ', '已打印', None, None, None))
    # Sheet2.save()
    print(Sheet2.shape)
    Sheet2.insertBlankLine(1)
    # Sheet2.getRow(15).Value = (('1', '1', '2018/3/29 11:23:26', '马玉', 'e06d5ebb-9b16-46aa-9462-a8ac00fbd36e', '增值税专用发票', '沈阳广盛鑫源商业投资管理有限公司', None, '咨询费', '600,000.00', '6.00%', '33,962.26', '566,037.74', '912101025507728654', '沈阳市和平区文萃路9号', '024-31077066', '盛京银行沈阳市科技支行', '0317010140940004025', None, '马玉', '瞿艺', '天职（北京）国际工程项目管理有限公司 ', '已打印', None, None, None))
    Sheet2.save()
