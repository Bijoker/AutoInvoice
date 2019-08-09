import os

import numpy as np
import pandas as pd
from pandas import DataFrame, Series


def getServiceType(path):
    '''
    获取商品名称
    :param path:
    :return:
    '''
    df = pd.read_csv(path,sep='~~',  encoding='gbk', header=2,skipinitialspace =True,engine='python')

    return  list(df['名称'])


def getSpecialTaxInvoice(path):
    df = pd.read_csv()

    pass

def getOrdinaryInvoice(path):

    pass


if __name__ == '__main__':
    path = r'D:\Downloads\商品编码.txt'
    data = getServiceType(path)
    print(data)