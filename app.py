#!/usr/bin/python
# -*-coding:utf-8-*-
import json
import sqlite3
from flask import Flask, session, request, render_template, redirect, url_for
import re
import pandas as pd
import numpy as np
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

@app.route('/')
def main_page():
    return render_template("login_page.html")

@app.route('/register',methods=['GET','POST'])
def register_page():
    return render_template("sign_up_page.html")

@app.route('/register_confirm',methods=['GET','POST'])
def register_confirm():
    register_name = str(request.values.get('name'))
    register_email = str(request.values.get("email"))
    register_password = str(request.values.get("password"))
    register_repassword = str(request.values.get("re-password"))
    # print(register_name, register_email, register_password, register_repassword )
    note = ""
    if not(len(register_name)<20 and len(register_name)>6) :
        note = note + "注册账户名长度不符合要求，长度应大于6个字符，小于20个字符！\n"

    # 检验用户名是否已经用过
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    exc = "select * from usr where usr_name = '%s' " % (register_name)
    list = cursor.execute(exc).fetchall()
    if len(list)!=0:
        note = note+"用户名已存在！\n"

    p = re.compile('^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')
    x =  p.match(register_email)
    if x != None:
        if x.group() != register_email:
            note = note + "邮箱格式输入错误！\n"
    else:
        note = note + "邮箱格式输入错误！\n"
    if not (len(register_password) > 6 and len(register_password)<20) :
        note = note + "登录密码长度不符合要求，长度应大于6个字符，小于20个字符！\n"
    if register_password != register_repassword:
        note = note + "两次输入密码不一致！\n"
    if len(note) != 0:
        return render_template("register-false.html", note=note)
    #print(register_name,register_email,register_password)
    cursor.execute("insert into usr(usr_name,usr_email,usr_password) values ('%s','%s','%s')"%(register_name,register_email,register_password))
    conn.commit()
    return render_template("login_page.html")

@app.route('/focus_index', methods=['GET','POST'])
def show_page():
    session["user_name"] = str(request.values.get('username'))
    user_name = session["user_name"]
    passwd = str(request.values.get('passwd'))
    session["password"] = passwd
    #print(user_name,passwd)
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    exc = "select * from usr where usr_name = '%s' and usr_password='%s'" % (session["user_name"],session["password"])
    list = cursor.execute(exc).fetchall()
    if len(list)!=0:
        return render_template("analyse_focus_index.html", username=session["user_name"])
    return render_template("register-false.html", note="用户名或密码输入错误")

@app.route('/analyse_page',methods=['GET','POST'])
def sex_page():
    from Sex_percent import get_sex_percent_main
    s,female,male=get_sex_percent_main()
    return render_template("analyse.html", user_name=session["user_name"],male=male,female=female)

@app.route('/analyse_page_place',methods=['GET','POST'])
def place_page():
    from place_percent import get_place_percent_main
    dir = get_place_percent_main()
    return render_template("analyse_2_place.html", user_name=session["user_name"],
                           data1=dir['北京'],data2 = dir['天津'],data3 = dir['上海'],data4 = dir['重庆'],data5 = dir['河北'],
                           data6 = dir['河南'],data7 = dir['云南'],data8 = dir['辽宁'],data9 = dir['黑龙江'],data10 = dir['湖南'],
                           data11 = dir['安徽'],data12 = dir['山东'],data13 = dir['新疆'],data14 = dir['江苏'],data15 = dir['浙江'],
                           data16 = dir['江西'],data17 = dir['湖北'],data18 = dir['广西'],data19 = dir['甘肃'],data20 = dir['山西'],
                           data21 = dir['内蒙古'],data22 = dir['陕西'],data23 = dir['吉林'],data24 = dir['福建'],data25 = dir['贵州'],
                           data26 = dir['广东'],data27 = dir['青海'],data28 = dir['西藏'], data29 = dir['四川'],data30 = dir['宁夏'],
                           data31 = dir['海南'],data32 = dir['台湾'],data33 = dir['香港'],data34 = dir['澳门'])

@app.route('/sex/json',methods=['POST'])
def sex_json():
    from Sex_percent import get_sex_percent_main
    data,female,male = get_sex_percent_main()
    return data

@app.route('/place/json',methods=['POST'])
def place_json():
    from place_percent import get_place_percent_main
    data = get_place_percent_main()
    print(data)
    return data

@app.route('/focus_index/json',methods=['POST'])
def focus_index_json():
    from weibo_focus_index import get_focus_main
    data = get_focus_main()
    return data

@app.route('/keyword',methods=['POST','GET'])
def focus_index_main():
    return render_template("analyse_keyword.html", user_name=session["user_name"])

@app.route('/keyword/json',methods=['POST'])
def get_keyword():
    from Keyword import get_keyword_json
    data = get_keyword_json()
    return data

@app.route('/keysentence/json',methods=['POST'])
def keysentence_json():
    from get_key_things import get_focus_things
    array = get_focus_things()
    arr1 = []
    for item in array:
        dir = {}
        dir["name"] = str(item)
        arr1.append(dir)
    dir1 = {}
    dir1["name"] = "微博"
    dir1["children"] = arr1
    arr2 = []
    arr2.append(dir1)
    dir2 = {}
    dir2["name"] = "热点分析"
    dir2["children"] = arr2
    arr3 = []
    arr3.append(dir2)
    s = json.dumps(arr3)
    return s

@app.route('/keysentence',methods=['POST','GET'])
def get_key_sentence():
    return render_template('analyse_keysentence.html',username = session["user_name"])

@app.route('/snlp',methods=['POST','GET'])
def snlp():
    from snlp import snlp_json
    # dir["极好"], dir["好"], dir["一般"], dir["差"], dir["极差"], total
    num1,num2,num3,num4,num5,total = snlp_json()
    return render_template('analyse_snlp.html',username =session["user_name"],num1=int((num1/total)*100),num2=int((num2/total)*100),num3=int((num3/total)*100),num4=int((num4/total)*100),num5=int((num5/total)*100),total=total)

@app.route('/k_means/place',methods=['POST','GET'])
def get_analyse_k_means_place():
    return render_template('analyse_k_means_place.html',username = session["user_name"])

@app.route('/k_means/json/get_lat_lng',methods=['POST'])
def json_get_lat_lng():
    loan_data = pd.DataFrame(pd.read_excel('data3.xlsx', header=0))
    loan_array = np.array(loan_data)
    array = []
    for item in loan_array:
        dir = {}
        lng = item[0]
        lat = item[1]
        province = item[2]
        city = item[3]
        dir["lng"] = lng
        dir["lat"] = lat
        dir["city"] = city
        array.append(dir)
    return json.dumps(array)


if __name__ == '__main__':
    app.run(host='0.0.0.0')