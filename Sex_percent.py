#!/usr/bin/python
# -*-coding:utf-8-*-
import json
import sqlite3
def get_sex_percent_main():
    conn = sqlite3.connect("weibo-spider-scrapy/weibo.sqlite3")
    cursor = conn.cursor()
    exc = "select name from sqlite_master where type='table' order by name"
    list = cursor.execute(exc).fetchall()
    male = 0
    female = 0
    for item in list:
        item = str(item)
        item = item[2:-3]
        # print(item)
        exc = "select user_sex from %s" %(item)
        sex_list = cursor.execute(exc).fetchall()
        for sex in sex_list:
            sex = str(sex)[2:-3]
            # print(sex)
            if sex=="女":
                female = female + 1
            if sex =="男":
                male = male + 1
    conn.commit()
    array = []
    dir = {}
    dir["性别"] = "女"
    dir["数量"] = female
    array.append(dir)
    dir = {}
    dir["性别"] = "男"
    dir["数量"] = male
    array.append(dir)
    s = json.dumps(array)
    return s,female,male