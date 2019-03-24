#!/usr/bin/python
# -*-coding:utf-8-*-
from textrank4zh import TextRank4Keyword
import sqlite3
import time
import json

def get_text(tablename):
    conn = sqlite3.connect('weibo-spider-scrapy/weibo.sqlite3')
    curs = conn.cursor()
    curs.execute("select content from %s" %(tablename))
    text = ""
    list = curs.fetchall()
    for item in list:
        item = str(item)[2:-3]
        text = text +  item + "\n"
    curs.close()
    return text

def insert_new_sql(SQLname,array):
    conn = sqlite3.connect('weibo-keywords.sqlite3')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE %s (word varchar (100),value varchar (100))' % (SQLname))
    for item in array:
        cursor.execute("insert into %s (word,value) values('%s','%s')" % (SQLname, str(item["word"]), str(item["weight"])))
        conn.commit()

def keyword(sqlname):
    text =get_text(sqlname)
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=text, lower=True, window=2)
    list = tr4w.get_keywords(num=100, word_min_len=2)
    i = 0
    array = []
    total = 0
    for w in list:
        if i>=10:
            break
        import jieba.posseg as pseg
        words = pseg.cut(w.word)
        for word, flag in words:
            w_word = word
            flag = flag
        if flag == "n" and w.word!="高铁" and w.word!="铁路" and w.word!="交通":
            dir = {}
            dir["word"] = w.word
            dir["weight"] = w.weight
            total = total + w.weight
            array.append(dir)
            i = i + 1
    for item in array:
        item["weight"] = int((item["weight"]/total)*100)
    return array

def get_keyword_json():
    from get_sql_name import get_sql_name_key
    SQLname = get_sql_name_key()
    conn = sqlite3.connect('weibo-keywords.sqlite3')
    cursor = conn.cursor()
    cursor.execute('select word,value from %s' % (SQLname))
    list = cursor.fetchall()
    array = []
    for word,weight in list:
        dir = {}
        dir["word"] = word
        dir["weight"] = weight
        array.append(dir)
    s = json.dumps(array)
    return s

def key_word_main():
    while True:
        now_time = time.strftime('%M', time.localtime(time.time()))
        if int(now_time) == "0" :
            from get_sql_name import get_sql_name_key
            sql_name = get_sql_name_key()
            array = keyword(sql_name)
            insert_new_sql(sql_name,array)
        time.sleep(60)
if __name__ == "__main__":
    key_word_main()
    # print(get_keyword_json())