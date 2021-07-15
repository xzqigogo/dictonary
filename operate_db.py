#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : operate_db.py
@Author: Piepis
@Date  : 2021/7/10 下午10:30
@Desc  : 
夏泽祺的程序
'''
"""
    该模块为dict项目中数据库数据处理模块，专门用作对数据库中内容的查找处理。
"""
import pymysql


class Database:
    def __init__(self, host='localhost',
                 port=3306,
                 user='root',
                 password='123456',
                 database='dict',
                 charset='utf8',
                 ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.connect_db()  # 连接数据库

    def connect_db(self):
        self.db = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                  password=self.password, database=self.database,
                                  charset=self.charset)

    # 创建游标函数（子进程单独创建）
    def create_cursor(self):
        self.cur = self.db.cursor()

    def cur_execute(self, sql):
        self.cur.execute(sql)

    def cur_fetchall(self):
        return self.cur.fetchall()

    def db_commit(self):
        self.db.commit()

    def db_rollback(self):
        self.db.rollback()

    def close(self):
        self.cur.close()
        self.db.close()
