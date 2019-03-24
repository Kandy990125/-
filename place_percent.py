#!/usr/bin/python
# -*-coding:utf-8-*-
import sqlite3
def get_place_percent_main():
    conn = sqlite3.connect("weibo-spider-scrapy/weibo.sqlite3")
    cursor = conn.cursor()
    exc = "select name from sqlite_master where type='table' order by name"
    list = cursor.execute(exc).fetchall()
    dir = {}
    array = []
    for item in list:
        item = str(item)
        item = item[2:-3]
        exc = "select user_stay_place from %s" %(item)
        place_list = cursor.execute(exc).fetchall()
        for place in place_list:
            place = str(place)[2:-3].split(' ')[0]
            if place not in dir.keys():
                dir[place] = 1
            else:
                dir[place] = dir[place] + 1
    return dir