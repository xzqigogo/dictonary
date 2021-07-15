#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : insert_words.py
@Author: Piepis
@Date  : 2021/7/9 下午6:37
@Desc  : 
夏泽祺的程序
'''
import pymysql
import re

fd = open('英汉词典TXT格式.txt', 'r')
db = pymysql.connect(user='root', password='123456', host='127.0.0.1',
                     port=3306, database='dict')
cur = db.cursor()
pos=0
# print(fd.readline().decode())
while True:
    data = fd.readline()
    if not data:
        break
    a = re.findall(r'(\S+)\s+(.+)', data)

    sql="insert into words (id,word,mean)values(%s,%s,%s)"
    # print(a[0][0],a[0][1])
    pos += 1
    # print(a[0])
    cur.execute(sql,[pos,a[0][0],a[0][1]])
try:
    db.commit()
except:
    db.rollback()
cur.close()
db.close()
