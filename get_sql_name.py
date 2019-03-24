#!/usr/bin/python
# -*-coding:utf-8-*-
import json
import sqlite3
import time
def get_sql_name():
    now_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    minute = str(int(int(time.strftime(time.strftime('%M', time.localtime(time.time())))) / 30) * 30)
    if len(minute) < 2:
        minute = "0" + minute
    recent_time = str(now_time[0:10]) + str(minute)
    sqlname = "weibo" + recent_time
    conn = sqlite3.connect("weibo-spider-scrapy/weibo.sqlite3")
    cursor = conn.cursor()
    exc = "select name from sqlite_master where type='table' order by name"
    list = cursor.execute(exc).fetchall()
    item_list = []
    for item in list:
        item_list.append(int(str(item)[7:-3]))
    item_list.sort()
    now = str(item_list[len(item_list)-1])[4:-4]
    print(now)
    return now,list
def get_sql_name_key():
    now_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    minute = str(int(int(time.strftime(time.strftime('%M', time.localtime(time.time())))) / 30) * 30)
    if len(minute) < 2:
        minute = "0" + minute
    recent_time = str(now_time[0:10]) + str(minute)
    sqlname = "weibo" + recent_time
    conn = sqlite3.connect("weibo-spider-scrapy/weibo.sqlite3")
    cursor = conn.cursor()
    exc = "select name from sqlite_master where type='table' order by name"
    list = cursor.execute(exc).fetchall()
    item_list = []
    for item in list:
        item_list.append(int(str(item)[7:-3]))
    item_list.sort()
    s = str(item_list[len(item_list) - 1])
    if s[-2:] == "00":
        s = s[:-2] + "00"
    s = "weibo" + s
    return s