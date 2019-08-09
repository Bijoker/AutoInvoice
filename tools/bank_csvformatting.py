import os
import re

def bankCsvformatting(path):
    '''
    银行csv文件格式化
    :param path:
    :return:
    '''
    try:
        with open(path, 'r', encoding='gbk') as f:
            data = f.read()
        # r'(?<=\d)(,)(?=\d)'
        pattern = re.compile(r'(?<=\d)(,)(?=\d)')
        newdata = re.sub(pattern, '', data).replace('"','').replace('\t', '').replace(',','|')
        print(newdata)
        os.remove(path)
        with open(path,'w', encoding='utf-8') as f:
            f.write(newdata)
        return True
    except Exception():
        pass

if __name__ == '__main__':
    path = r'D:\Downloads\historydetail1243.csv'
    bankCsvformatting(path)