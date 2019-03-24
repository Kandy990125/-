#!/usr/bin/python
# -*-coding:utf-8-*-
import json
import sqlite3
import time
def get_focus_main():
    from get_sql_name import get_sql_name
    conn = sqlite3.connect("weibo-spider-scrapy/weibo.sqlite3")
    cursor = conn.cursor()
    now,list = get_sql_name()
    array = []
    i = 0
    while i < len(list)-1:
        i = i + 1
        item = list[i-1]
        if str(item)[11:-7] != now:
            continue
        if str(item)[17:-3] == "30":
            continue
        dir = {}
        dir["time"] = str(item)[15:-5] + ":" + str(item)[17:-3]
        exc = "select user_sex from %s" % (str(item)[2:-3])
        sex_list = cursor.execute(exc).fetchall()
        x = len(sex_list)
        female = 0
        male = 0
        for sex in sex_list:
            sex = str(sex)[2:-3]
            if sex == "女":
                female = female + 1
            if sex == "男":
                male = male + 1

        exc = "select user_sex from %s" % (str(list[i])[2:-3])
        sex_list = cursor.execute(exc).fetchall()
        dir["index"] = x + len(sex_list)
        for sex in sex_list:
            sex = str(sex)[2:-3]
            if sex == "女":
                female = female + 1
            if sex == "男":
                male = male + 1
        dir["male"] = male
        dir["female"] = female
        array.append(dir)
    conn.commit()
    s = json.dumps(array)
    return s