#!/usr/bin/python
# -*-coding:utf-8-*-
import sqlite3
from snownlp import SnowNLP
import time
import operator
def get_snlp_index():
    from get_sql_name import get_sql_name_key
    sqlname  = get_sql_name_key()
    conn = sqlite3.connect('weibo-spider-scrapy/weibo.sqlite3')
    curs = conn.cursor()
    curs.execute("select blog_id,usr_id,user_name,content,reposts_count,comments_count,attitudes_count from %s" % (sqlname))
    list = curs.fetchall()
    array = []
    for item in list:
        s = SnowNLP(item[2])
        i = 0
        sum = 0
        for sentence in s.sentences:
            # print(sentence)
            s = SnowNLP(sentence)
            # print(sentence,s.sentiments)
            i = i + 1
            sum = sum + s.sentiments
        avg = sum / i
        dir = {}
        dir["blog_id"] = str(item[0])
        dir["user_id"] = str(item[1])
        dir["user_name"] = item[2]
        dir["content"] = item[3]
        dir["reposts_count"] = item[4]
        dir["comments_count"] = item[5]
        dir["attitudes_count"] = item[6]
        dir["value"] = avg
        array.append(dir)
    return array

def insert_item(array,SQLname):
    conn = sqlite3.connect('weibo-snlp.sqlite3')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE %s (blog_id varchar(100),user_id varchar(100),user_name varchar (100),content varchar (1000),reposts_count varchar (10),comments_count varchar (10),attitudes_count varchar (10),value varchar (100))' % (SQLname))
    for dir in array:
        cursor.execute(
            "insert into %s (blog_id,user_id,user_name,content,reposts_count,comments_count,attitudes_count,value) values('%s','%s','%s','%s','%s','%s','%s','%s')" % (SQLname, dir["blog_id"],dir["user_id"],dir["user_name"],dir["content"],dir["reposts_count"],dir["comments_count"],dir["attitudes_count"],dir["value"]))
        conn.commit()
def snlp_main():
    while True:
        now_time = time.strftime('%M', time.localtime(time.time()))
        if int(now_time) == "0" :
            from get_sql_name import get_sql_name_key
            array = get_snlp_index()
            sqlname = get_sql_name_key()
            insert_item(array, sqlname)
        time.sleep(60)

def snlp_json():
    from get_sql_name import get_sql_name_key
    sqlname = get_sql_name_key()
    conn = sqlite3.connect('weibo-snlp.sqlite3')
    cursor = conn.cursor()
    cursor.execute('select blog_id,user_id,user_name,content,reposts_count,comments_count,attitudes_count,value from %s' % (sqlname))
    list = cursor.fetchall()

    myarray = []
    for item in list:
        mydir = {}
        mydir["content"] = item[3]
        mydir["user_id"] = item[1]
        mydir["user_name"] = item[2]
        mydir["count"] = int(item[4])+int(item[5])+int(item[6])
        mydir["value"] = item[7]
        myarray.append(mydir)
    # x = [{'name': 'Homer', 'age': 39}, {'name': 'Bart', 'age': 10}]
    sorted_myarray = sorted(myarray, key=operator.itemgetter('value'))
    print_array = []
    i = 0
    for item in sorted_myarray:
        if i>=10:
            break
        flag = 1
        for print_item in print_array:
            if item["content"] == print_item["content"]:
                flag= 0
                break
        if flag==0:
            continue
        print_dir = {}
        print_dir["content"] = item["content"]
        print_dir["user_id"] = item["user_id"]
        print_dir["user_name"] = item["user_name"]
        print_array.append(print_dir)
        i = i + 1
    # for item in print_array:
    #         print(item)
    total = len(list)
    array = []
    dir = {}
    dir["极好"] = 0
    dir["好"] = 0
    dir["一般"] = 0
    dir["差"] = 0
    dir["极差"] = 0
    for item in list:
        value = float(item[7])
        if value>=0 and value<0.2:
            dir["极差"] = dir["极差"] + 1
        if value>=0.2 and value<0.4:
            dir["差"] = dir["差"] + 1
        if value>=0.4 and value<0.6:
            dir["一般"] = dir["一般"] + 1
        if value>=0.6 and value<0.8:
            dir["好"] = dir["好"] + 1
        if value>=0.8 and value<=1:
            dir["极好"] = dir["极好"] + 1
    return dir["极好"],dir["好"],dir["一般"],dir["差"],dir["极差"],total
if __name__ == "__main__":
    # snlp_main()
    snlp_json()