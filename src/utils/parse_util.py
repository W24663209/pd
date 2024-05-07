import json

import openpyxl
import requests
from utils import mysql_util
import concurrent.futures


def save(item):
    url = 'https://webhook.kingpay.io/api/providusbank/payin'
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(item), headers=headers)
    print(response.text)


def xlsx(path):
    # 打开Excel文件
    workbook = openpyxl.load_workbook(path)
    # 选择要读取的工作表
    sheet = workbook.active
    # 读取单元格数据示例
    # cell_value = sheet['A1'].value
    # print("Value in cell A1:", cell_value)
    # 遍历行示例
    index = 0
    rows = sheet.iter_rows(values_only=True)
    max_row = rows.gi_frame.f_locals['max_row']
    thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    # for text in open('src/download/STATEMENT.csv').read().split('\n')[19:-5]:
    #     pass
    for row in rows:
        if index >= 17 and max_row - 4 >= index:
            item = {}
            item['postDate'] = row[0]
            item['actualTransactionDate'] = row[1]
            item['narration'] = row[2].replace('INWARD TRANSFER', '').replace('FROM', '')
            item['valueDate'] = row[3]
            item['debit'] = row[4]
            item['credit'] = row[5]
            item['currentBalance'] = row[6]
            item['drCr'] = row[7]
            item['docNum'] = row[8]
            thread_pool.submit(save, item)
        index += 1
    # 关闭Excel文件
    workbook.close()
    thread_pool.shutdown(wait=True)


if __name__ == '__main__':
    xlsx('../../src/download/STATEMENT.xlsx')
