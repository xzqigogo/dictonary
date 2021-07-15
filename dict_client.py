#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : dict_client.py
@Author: Piepis
@Date  : 2021/7/10 下午11:56
@Desc  : 
夏泽祺的程序
'''
import time

"""
dict 客户端
客户端要求：
*输入注册信息
*将信息发送给服务端
*等待反馈
"""

import sys
from socket import *
import getpass
import re

# 定义全局变量
HOST = '0.0.0.0'
PORT = 8899
ADDR = (HOST, PORT)
s = socket(AF_INET, SOCK_STREAM, proto=0)
s.connect(ADDR)


def main_interface():
    print("===============================================")
    print("   1.注册           2.登录              3.退出   ")
    print("===============================================")


def do_register():
    # 注册函数，用于用户首次登录的注册
    while True:
        try:
            tmp = True
            name = input("请输入索要创建账号名称:")
            if " " in name:
                print("账号不能有空格，请重新输入")
                continue
            for item in name:
                if u'\u4e00' < item < u'\u9fff':
                    print("账号不能有中文,请重新输入")
                    tmp = False
                    break
            if tmp == False:
                continue
            else:
                while True:
                    passwd = getpass.getpass("请输入密码:")
                    if ' ' in passwd:
                        print("密码不能有空格，请重新输入密码")
                        continue
                    else:
                        passwd1 = getpass.getpass("请再次输入密码:")
                        if passwd1 != passwd:
                            print("两次密码不一致请重新输入")
                            continue
                        else:
                            break
            msg = "R %s %s" % (name, passwd)
            print(msg)
            # 将注册协议发送至服务端
            s.send(msg.encode())
            data = s.recv(128).decode()
            if data == 'ok':
                print("注册成功")
                return
            else:
                print("注册失败")
                print("是否要返回上一级?----1.返回；2.继续注册")
                while True:
                    try:
                        option = input()
                        if option == 1:
                            return
                        elif option == 2:
                            break
                        else:
                            print("输入错误请重新输入")
                    except KeyboardInterrupt:
                        sys.exit("程序已退出")
        except KeyboardInterrupt:
            sys.exit("程序已退出")


def show_dict():
    while True:
        print("=====================================")
        print("=======欢迎来到英汉字典查询界面===========")
        print("=======1.查询单词======================")
        print("=======2.查看历史记录===================")
        print("=======3.退出登录======================")
        print("=====================================")
        try:
            opition=input("请输入选项")
            if opition=='1':
                time.sleep(0.1)
                s.send(b'1')
                check_words()
            elif opition=='2':
                time.sleep(0.1)
                s.send(b'2')
                check_hist()
            elif opition=='3':
                time.sleep(0.1)
                s.send(b'q')
                return
        except KeyboardInterrupt:
            sys.exit('程序已退出')

def check_hist():
    hist=s.recv(2048).decode()
    print(hist)


def check_words():
    while True:
        try:
            word = input("请输入你要查询的单词"
                         ">>")
        except KeyboardInterrupt:
            sys.exit('客户端已退出')
        if word == 'q':
            time.sleep(0.1)
            s.send(b'quit')
            return
        else:
            time.sleep(0.1)
            s.send(word.encode())
            mean = s.recv(1024).decode()
            print("%s的意思是:\n%s" % (word, mean))


def do_login():
    s.send("L ".encode())
    data = s.recv(2048).decode()
    info_list = re.findall(r'(\S+)\s(\w+)', data)
    while True:
        try:
            name = input("请输入账号:")
            password = getpass.getpass("请输入密码:")
        except KeyboardInterrupt:
            sys.exit('客户端已瑞出')
        # print(info_list)#测试：从客户端口打印数据库中所有用户
        tag = True
        for item in range(len(info_list)):
            if info_list[item][0] == name:
                if info_list[item][1] == password:
                    print("登录成功")
                    s.send(name.encode())
                    show_dict()
                    return
                else:
                    tag = False
        if tag == True:
            print("尚未有该账户，请核对账户名称或者注册账户")
        else:
            print("密码错误，请重新登录")


def main():
    # 主函数，用于与服务端连接
    s.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
    while True:
        main_interface()
        option = input("请输入你要操作的选项:")
        if option == '1':
            do_register()
        elif option == '2':
            do_login()
        elif option == '3':
            s.send(b'bye')
            sys.exit("已退出，欢迎下次再来")
        else:
            print("输入错误，请重新输入")
            continue


if __name__ == '__main__':
    main()
