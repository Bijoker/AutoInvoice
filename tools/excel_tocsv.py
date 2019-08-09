import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import os

def excelToCsv(path, sep):
    pd.set_option('display.max_columns', None)
    io = pd.io.excel.ExcelFile(path)
    sheetnames = io.sheet_names
    print(sheetnames)
    data = []
    for sheetname in sheetnames:
        # data.append(pd.read_excel(path, sheet_name=sheetname,dtype='str'))
        df = pd.read_excel(io, sheet_name=sheetname, dtype='str')
        data.append(df)
    df = pd.concat(data)
    print(df.shape)
    print(df.dtypes)
    newfilename = os.path.join(os.path.split(path)[0],os.path.splitext(os.path.basename(path))[0] + '.csv')
    df.to_csv(newfilename, sep=sep, encoding='utf-8', index=False)
    io.close()
    return newfilename

if __name__ == '__main__':
    path = r'D:\Downloads\回款信息20190612141034.xls'
    excelToCsv(path, '|')