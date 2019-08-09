import requests,json

def javePost(*args, **kwargs):
    url = 'http://172.16.207.238:8080/ccyboa_service/common/insert'
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(kwargs['payload']), headers=headers)
    print(r.status_code, r.text)
    if r.status_code == '200':
        return 'ok'
    else:
        return r.status_code, r.text




if __name__ == '__main__':
    url = 'http://172.16.207.238:8080/ccyboa_service/common/insert'


    #银行数据
    backPayload = {
        "inFileName": "银行.csv",
        "inFilePath": "D://invoice//download//",
        "tableName": "ops_data_bank",
        "inTemplateName": "ICBCStatmentImportTemplate",
        "batchName": "TZCPA_ECP_INVOICE_PAYMENT_DETAILS",
        "batchUniqueCode": "0200283119201026872"
    }
    #开票数据

    a = {
        'inFileName': '开票信息20190619161529.csv',
        'inFilePath': 'D://invoice//download//',
        'tableName': 'ops_data_invoice_payment',
        'inTemplateName': 'InvoiceDetailTemplate',
        'batchName': 'ICBC_STATEMENT',
        'batchUniqueCode': '0200283119201026872'
    }
    javePost(payload=a)
