import os
import datetime
import pymysql
import numpy as np
import pandas as pd
from pandas import DataFrame,Series

from tools.log_init import Log

pd.set_option('display.max_columns', None)
log = Log()



def GenerateReports2(path,start,end):

    start = datetime.datetime.strptime(start,'%Y/%m/%d').strftime('%Y-%m-%d')
    end = datetime.datetime.strptime(end,'%Y/%m/%d').strftime('%Y-%m-%d')
    log.info('start: %s \n end:%s' %(start,end))
    conn = pymysql.connect('172.16.207.72', 'root', 'root', 'invoiceverfy', charset='utf8')
    cursor = conn.cursor()
    sql = '''SELECT

	b.projectId ,
	a.data_datetime_1 ,
	a.data_comment_8 ,
	a.data_decimal_2 ,
	
IF ( b.invoiceNumber IS NULL, '预收账款', '应收账款' ) ,
	'现金' ,
	'天职国际会计师事务所（特殊普通合伙）' ,
	'总部' ,
	'200400108' ,
	IFNULL( 
	b.invoiceNumber
	, '00000000' ) ,
	b.invoiceAmount,
	b.receiveMoney,
	b.cumulative,
	a.data_comment_9
FROM
	ops_data_bank a
	LEFT JOIN ( 	select * from (SELECT v_invoiceinfo.*, v_invoiceinfo.invoiceAmount - v_invoiceinfo.receiveMoney AS cumulative FROM v_invoiceinfo where  v_invoiceinfo.invoiceAmount <> v_invoiceinfo.receiveMoney) c 
	GROUP BY  c.units , c.cumulative ) b ON a.data_comment_8 = b.units 
	AND a.data_decimal_2 = b.cumulative 
WHERE
	a.data_decimal_2 IS NOT NULL and a.data_datetime_1 BETWEEN  '%s 00:00:00'  AND '%s 23:59:59'
ORDER BY
	a.data_comment_8 DESC,
	b.projectId ASC''' %(start,end)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception('sql执行错误') as e:
        print(e)
    cursor.close()
    conn.close()

    log.info(results)
    df = pd.DataFrame(np.array(results),
                      columns=['项目编号', '回款日期', '回款单位名称', '银行到账金额', '回款类型', '回款方式', '收款单位', '收款单位所属机构', '收款登记人', '发票编号','开票金额', '累计已回款', '开票-回款', '备注'])

    log.info(df)
    df.to_excel(path, index=False)


def GenerateReports(path, start, end):
    start = datetime.datetime.strptime(start, '%Y/%m/%d').strftime('%Y-%m-%d')
    end = datetime.datetime.strptime(end, '%Y/%m/%d').strftime('%Y-%m-%d')


    conn = pymysql.connect('172.16.207.72', 'root', 'root', 'invoiceverfy', charset='utf8')
    df1 = pd.read_sql("""
    
    
    SELECT * FROM (
    SELECT
        k.data_id,
        k.data_comment_2,
        k.data_comment_10,
        k.data_comment_7,
        k.data_comment_1,
        k.data_decimal_1,	
        (SELECT
        SUM( h.data_decimal_1 ) AS moneyBack 
    FROM
        ops_data_invoice_payment_details h 
    WHERE
        h.is_delete = 0 
        AND h.data_comment_6 = '应收账款'
        AND k.data_comment_2 = h.data_comment_2 
        AND k.data_comment_10 = h.data_comment_5 
        AND k.data_comment_7 = h.data_comment_12 
    GROUP BY
        h.data_comment_2,
        h.data_comment_5,
        h.data_comment_12 
        ) difference
    FROM
        ops_data_invoice_payment k 
    WHERE
        k.is_delete = 0 
        AND k.data_comment_13 = '已开票' 
        AND k.data_comment_6 <> '营业税发票' 
        )
        differenceTable WHERE ISNULL(differenceTable.difference) 
        AND  EXISTS(SELECT data_comment_8 FROM ops_data_bank b WHERE b.is_delete=0 AND b.data_comment_8=differenceTable.data_comment_10) 
    """,conn)
    df1['money'] = 0.0
    df1['backMoneyTime'] = None
    df1['backMoneyTime'] = df1['backMoneyTime'].astype('datetime64')


    df2 = pd.read_sql('''
    
SELECT b.data_datetime_1,b.data_comment_8,SUM(data_decimal_2) bankmoney , b.data_comment_9 FROM ops_data_bank b WHERE b.is_delete = 0 AND b.data_datetime_1 BETWEEN '%s 00:00:00'  AND '%s 23:59:59' AND LOCATE('天职国际', b.data_comment_8) = 0 GROUP BY b.data_comment_8
    ''' %(start, end), conn)
    conn.close()

    for row in range(df1.shape[0]):
        #     print(df2[ df2['data_comment_8'] == df1.loc[index]['data_comment_10']])
        invoicemoney = df1.loc[row]['data_decimal_1']
        bankmoney = df2[df2['data_comment_8'] == df1.loc[row]['data_comment_10']]['bankmoney']

        backmoneytime = (df2.loc[bankmoney.index]['data_datetime_1']).iloc[0]

        flag = (df2.loc[bankmoney.index]['bankmoney'] >= invoicemoney).iloc[0]
        if flag:
            df1.loc[row, 'money'] = invoicemoney
            df1.loc[row, 'backMoneyTime'] = backmoneytime.strftime('%Y/%m/%d')
            df2.loc[df2['data_comment_8'] == df1.loc[row]['data_comment_10'], 'bankmoney'] = bankmoney - invoicemoney

    df2 = df2[df2['bankmoney'] != 0.0]
    df1 = df1[df1['money'] != 0.0]

    df1 = df1.drop(columns=['data_id','data_comment_7','difference'])
    df1['invoicetype'] = '应收账款'
    df1['paymentmethod'] = '银行转账'
    df1['RegistrarofReceivables'] = '200300081'
    df1['ReceivingUnit'] = '天职国际会计师事务所（特殊普通合伙）'
    df1['DepartmentsofReceivingUnits'] = '总所'

    order = ['data_comment_2','backMoneyTime','data_comment_10','money','invoicetype','paymentmethod','ReceivingUnit','DepartmentsofReceivingUnits','RegistrarofReceivables','data_comment_1'   ]
    df1 = df1[order]

    df1.columns = ['项目编号', '回款日期', '回款单位名称', '回款金额', '回款类型', '回款方式', '收款单位', '收款单位所属机构', '收款登记人', '发票编号']
    df1.to_excel(path, index=False)
    CollectInAdvance = df2.copy()
    CollectInAdvance['data_datetime_1'] = CollectInAdvance['data_datetime_1'].apply(lambda x: x.strftime('%Y/%m/%d'))
    CollectInAdvance['ItemNumber'] = None
    CollectInAdvance['invoiceNumber'] = '00000000'
    CollectInAdvance['invoicetype'] = '预收账款'
    CollectInAdvance['paymentmethod'] = '银行转账'
    CollectInAdvance['RegistrarofReceivables'] = '200300081'
    CollectInAdvance['ReceivingUnit'] = '天职国际会计师事务所（特殊普通合伙）'
    CollectInAdvance['DepartmentsofReceivingUnits'] = '总所'

    order = ['ItemNumber', 'data_datetime_1', 'data_comment_8', 'bankmoney', 'invoicetype', 'paymentmethod',
             'ReceivingUnit', 'DepartmentsofReceivingUnits', 'RegistrarofReceivables', 'invoiceNumber',
             'data_comment_9']
    CollectInAdvance = CollectInAdvance[order]
    CollectInAdvance.columns = ['项目编号', '回款日期', '回款单位名称', '回款金额', '回款类型', '回款方式', '收款单位', '收款单位所属机构', '收款登记人', '发票编号', '备注']
    CollectInAdvance.to_excel(os.path.splitext(path)[0] + '预收' + os.path.splitext(path)[1], index=False)



if  __name__ == '__main__':

    path = r'a.xlsx'
    GenerateReports(path,'2019/7/15', '2019/7/16')

