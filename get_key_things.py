#!/usr/bin/python
# -*-coding:utf-8-*-
import sqlite3
from get_sql_name import get_sql_name_key
from textrank4zh import TextRank4Keyword
def get_focus_things():
    array = []
    conn = sqlite3.connect('weibo-spider-scrapy/weibo.sqlite3')
    tablename = get_sql_name_key()
    curs = conn.cursor()
    curs.execute("select blog_id,content,reposts_count,comments_count,attitudes_count from %s" % (tablename))
    list = curs.fetchall()
    for info in list:
        total = int(info[2]) + int(info[3]) + int(info[4])
        if total>=100:
            content = info[1]
            tr4w = TextRank4Keyword()
            tr4w.analyze(text=content, lower=True, window=2)
            phrase = tr4w.get_keyphrases(keywords_num=20, min_occur_num=3)
            for p in phrase:
                if str(p)=="生殖器挂":
                    continue
                if p not in array:
                    array.append(p)
    curs.close()
    return array