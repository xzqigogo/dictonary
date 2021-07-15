#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : dict_server.py
@Author: Piepis
@Date  : 2021/7/10 下午11:56
@Desc  : 
夏泽祺的程序
'''
import sys
import time

"""
dict服务端
处理请求逻辑
"""

from socket import *
from multiprocessing import Process
import signal
from operate_db import *

# 全局变量定义
HOST = '0.0.0.0'
PORT = 8899
ADDR = (HOST, PORT)


def server_register(c, datasp, db):
    sql = "insert into user (name,password) values ('%s','%s');" % (datasp[1], datasp[2])
    # print(sql)
    db.create_cursor()
    try:
        db.cur_execute(sql)
        # print("执行了sql")
        db.db_commit()
        c.send(b'ok')
        return
    except:
        db.db_rollback()
        c.send(b'no')


def server_login(c, db):
    # 先检查客户端输入的信息是否在数据库中存在
    str = " "
    sql1 = "select name,password from user"
    db.create_cursor()
    db.cur_execute(sql1)
    data = db.cur_fetchall()
    for item in range(len(data)):
        str += "%s %s\n" % (data[item][0], data[item][1])
    c.send(str.encode())
    name = c.recv(1024).decode()
    while True:
        option = c.recv(128).decode()
        if option == 'q' or not option:
            return
        elif option == '1':
            check_word(c, name, db)
        elif option == '2':
            check_hist(c, name, db)



def check_hist(c, name, db):
    ########如下为查询该账户check history
    sql3 = "select word,time from hist where name='%s'" % name
    str = ''
    db.cur_execute(sql3)
    hist = db.cur_fetchall()
    for item in hist:
        str += (item[0] + ' ' + item[1].strftime('%Y-%m-%d') + '\n')
    c.send(str.encode())

    ########如下为服务端接收到客户端传来的需要查询的单词


def check_word(c, name, db):
    while True:
        word = c.recv(1024).decode()
        if word == "quit":
            return
        sql2 = "select mean from words where word='%s'" % word
        sql3 = "insert into hist(name,word,time) values('%s','%s',now())" % (name, word)
        # print(sql3)
        try:
            db.cur_execute(sql2)
            data = db.cur_fetchall()
            c.send(data[0][0].encode())
            db.cur_execute(sql3)
            db.db_commit()
        except:
            c.send('词库中没有该单词'.encode())
            continue


def handle(c, db):
    # 接收到客户端发来的注册协议，并通过字符串拆分解读协议
    while True:
        data = c.recv(1024).decode()
        datasp = data.split(' ')
        if not data or datasp[0]=="bye":
            sys.exit('user is quit')
        elif datasp[0] == 'R':
            server_register(c, datasp, db)
        elif datasp[0] == "L":
            server_login(c, db)



def main():
    # 创建套接字
    db = Database()
    db.connect_db()
    s = socket(AF_INET, SOCK_STREAM, proto=0)
    s.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
    s.bind(ADDR)
    s.listen(5)
    print("waiting for connect......")
    while True:
        try:
            c, addr = s.accept()
            print("connect from :", addr)
        except KeyboardInterrupt:
            sys.exit('服务端已退出')
        except Exception as e:
            print(e)
            continue

        # 创建子进程
        p = Process(target=handle, args=(c, db,))
        p.daemon = True  # 父进程结束，子进程也随之结束
        p.start()


if __name__ == '__main__':
    main()
