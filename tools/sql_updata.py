import os
import pandas as pd
from pandas import DataFrame,Series
import pymysql

from tools.log_init import Log

log = Log()

def insert0ps_data_bank(key,path):
    '''

    :param key:  invoicePyload:开票信息，  backMoneyload：回款信息，  bankPayload：银行信息
    :param path:
    :return:
    '''

    log.info('连接MYSQL数据库')
    conn = pymysql.connect('172.16.207.72', 'root', 'root', 'invoiceverfy', charset='utf8')
    cursor = conn.cursor()

    #开票信息
    if key == 'invoicePyload':
        log.info('准备上传开票信息')


        sql = '''
            UPDATE %s SET is_delete=1  WHERE is_delete = 0
            ''' % 'ops_data_invoice_payment'
        try:
            cursor.execute(sql)
            conn.commit()
            log.info('sql数据逻辑删除成功')
        except:
            log.info('数据库逻辑删除失败')
            conn.rollback()
            log.info('数据库回滚')

        log.info('上传开票信息')
        def gormat(x):
            if x.replace(' ', '') == '':
                return 0
            else:
                return str(x)
        df = pd.read_csv(path,sep='|', header=0, na_filter=False, dtype='str')
        df['发票含税金额(元)'] = df['发票含税金额(元)'].apply(gormat)
        values = df.values.tolist()
        sql = "INSERT INTO ops_data_invoice_payment(data_int_1, data_comment_1, data_comment_2, data_comment_3, data_comment_4, data_comment_5, data_comment_6, data_comment_7, data_comment_8, data_comment_9, data_comment_10, data_decimal_1, data_comment_11, data_comment_12, data_comment_13,data_comment_14, data_comment_15) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        try:
            cursor.executemany(sql,values)
            conn.commit()
        except Exception as e:
            log.warning(e)
            conn.rollback()


    #上传回款信息
    elif key == "backMoneyload":
        log.info('准备上传回款信息')

        sql = '''
                   UPDATE %s SET is_delete=1  WHERE is_delete = 0
                   ''' % 'ops_data_invoice_payment_details'
        try:
            cursor.execute(sql)
            conn.commit()
            log.info('sql数据逻辑删除成功')
        except:
            log.info('数据库逻辑删除失败')
            conn.rollback()
            log.info('数据库回滚')

        log.info('上传回款信息')
        def gormat(x):
            if x.replace(' ', '') == '':
                return 0
            else:
                return str(x)
        df = pd.read_csv(path, sep='|', header=0, na_filter=False, dtype='str')
        df['回款金额(元)'] = df['回款金额(元)'].apply(gormat)
        values = df.values.tolist()
        sql = "INSERT INTO ops_data_invoice_payment_details(data_int_1, data_comment_1, data_comment_2, data_comment_3, data_comment_4, data_comment_5, data_decimal_1, data_comment_6, data_comment_7, data_comment_8, data_comment_9, data_comment_10, data_comment_11, data_comment_12, data_comment_13) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        try:
            cursor.executemany(sql, values)
            conn.commit()
            log.info('sql数据逻辑删除成功')
        except:
            log.info('数据库逻辑删除失败')
            conn.rollback()
            log.info('数据库回滚')


    #上传银行信息
    elif key == 'bankPayload':
        log.info('准备上传银行信息')

        sql = '''
                      UPDATE %s SET is_delete=1  WHERE is_delete = 0
                      ''' % 'ops_data_bank'
        try:
            cursor.execute(sql)
            conn.commit()
            log.info('sql数据逻辑删除成功')
        except:
            log.warning('数据逻辑删除失败')
            conn.rollback()
            log.info('数据回滚')

        log.info('上传银行信息')
        def gormat(x):
            if x.replace(' ', '') == '':
                return 0
            else:
                return str(x)
        df = pd.read_csv(path, sep='|',header=1, na_filter=False, dtype='str')
        df['借方发生额'] = df['借方发生额'].apply(gormat)
        df['贷方发生额'] = df['贷方发生额'].apply(gormat)
        df['余额'] = df['余额'].apply(gormat)
        values = df.values.tolist()
        sql = "INSERT INTO ops_data_bank(data_comment_1, data_comment_2, data_comment_3, data_datetime_1, data_comment_4, data_decimal_1, data_decimal_2, data_comment_5, data_comment_6, data_comment_7, data_comment_8,  data_decimal_3, data_comment_9) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s);"
        try:
            cursor.executemany(sql, values)
            conn.commit()
        except Exception as e:
            log.warning(e)
            conn.rollback()
    else:
        log.warning('输入key错误')
        return Exception('输入key错误')
    cursor.close()
    conn.close()


if __name__ == '__main__':
    # invoicePyload: 开票信息，  backMoneyload：回款信息，  bankPayload：银行信息
    path1 = r'D:\Desktop\tzcpa\BJinvoice\invioceveify\backup\invoice\开票信息20190709143246.csv'
    path2 = r'D:\Desktop\tzcpa\BJinvoice\invioceveify\backup\moneyback\回款信息20190709143257.csv'
    path3 = r'D:\Desktop\tzcpa\BJinvoice\invioceveify\backup\bankRunningWater\historydetail11130.csv'
    # insert0ps_data_bank('invoicePyload',path1)
    # insert0ps_data_bank('backMoneyload', path2)
    insert0ps_data_bank('bankPayload', path3)





