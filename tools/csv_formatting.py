import re,os

def csvFormatting(path):
    '''
    将csv数据进行处理，删除空格，删除字符串中的 \n
    :param path:  sep = |
    :return:
    '''

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = f.read()
        newdata = re.sub(re.compile(re.compile(r'\n+\||\|\n+ |"\n+|\n+"')), '', data.replace(' ', ''))
        os.remove(path)
        with open(path,'w', encoding='utf-8')  as f:
            f.write(newdata)
        return True
    except Exception():
        pass
if __name__ == '__main__':
    path = r'D:\Desktop\tzcpa\BJinvoice\invioceveify\backup\bankRunningWater\historydetail2016.csv'
    csvFormatting(path)
