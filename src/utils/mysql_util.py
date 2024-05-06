#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   mysql_util.py
@Description TODO 数据库连接工具
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/8/3 18:59:17   weizongtang      1.0         None
'''
import pymysql
import re

#     url: jdbc:p6spy:mysql://172.31.9.86:3306/otpay?useUnicode=true&characterEncoding=UTF-8&serverTimezone=Asia/Shanghai&allowPublicKeyRetrieval=true&verifyServerCertificate=false&useSSL=false
#     username: root
#     password: fhdjewu465fhd00kewe
# conn = pymysql.connect(host=“你的数据库地址”, user=“用户名”,password=“密码”,database=“数据库名”,charset=“utf8”)

# con = pymysql.connect(host='100.126.125.107', port=3306, user='root', password='fhdjewu465fhd00kewe',
#                       database='otpay',
#                       charset='utf8')
from dbutils.pooled_db import PooledDB

# 创建数据库连接池
pool = PooledDB(pymysql, 5, host='100.126.125.107', user='root', password='fhdjewu465fhd00kewe', database='otpay')


def one(sql):
    connection = pool.connection()
    cur = connection.cursor()
    cur.execute(sql + ' limit 1')
    fetchone = cur.fetchone()
    cur.close()
    return fetchone


def list(sql):
    connection = pool.connection()
    cur = connection.cursor()
    cur.execute(sql)
    all = cur.fetchall()
    cur.close()
    return all

def update(sql):
    connection = pool.connection()
    cur = connection.cursor()
    cur.execute(sql)
    # 提交更改
    connection.commit()
    cur.close()


if __name__ == '__main__':
    # for id,amount,payout_bank_account_number,merchant_account_number in list('select id,amount,payout_bank_account_number,merchant_account_number from tbl_merchant_payout where status=4 and channel_id=275'):
    #     print(id,amount,payout_bank_account_number,merchant_account_number)
    update("update tbl_kes_accounts set balance=200 where user_account='115188831'")