#coding=utf-8
import os
from flask import Flask
from flask import request
from flask_cors import CORS

from sqlalchemy import create_engine
from lichangbo_createDB import engine,Chat,Users,Limin,News,Service
from  sqlalchemy.orm import sessionmaker

import requests
import json 



app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

CORS(app)
#廣播功能
@app.route("/broadcast/<msg>")
def broadcast(msg):
    url = 'https://api.line.me/v2/bot/message/broadcast'
    headers = {
    'Content-Type':'application/json',
    'Authorization':'Bearer Qw41For/uMNtw6fWwFF//qbHp7ThrQCckmZP47PtUyKk8Bk7jQl1gXF4mjfUXQrQB2smf7Dx1ZqeZv6Ggtwyta6zhe6Nzn+EPtkiOrv992qJoayHtFn5ORyB9GEXIdVGLxqu+ISyZYCk/6+45Qv5xAdB04t89/1O/w1cDnyilFU='
    }
    
    data = {
        
        "messages": [
            {
                "type": "text",
                "text": "%s"%(msg)
            }
        ]
    }
    r = requests.post(url=url,headers=headers,data = json.dumps(data))

    print(r.status_code)

#聊天紀錄
@app.route("/chat_history")
def query():
    list_chat_history = []
    '''与数据库建立链接'''
    engine = create_engine("mysql+pymysql://root:qd513020@localhost:3306/agent",echo=True)

    # 创建会话
    session = sessionmaker(engine)
    mySession = session()

    '''
    for room_id, line_user_id, line_user_text, web_cov_text, time in mySession.query(Chat.room_id, Chat.line_user_id, Chat.line_user_text, Chat.web_cov_text, Chat.time):
        print(room_id, line_user_id, line_user_text, web_cov_text, time)
        list_chat_history.append(room_id)
        list_chat_history.append(line_user_id)
        list_chat_history.append(line_user_text)
        list_chat_history.append(web_cov_text)
        list_chat_history.append(time)
        print(list_chat_history)
        result = { 'chat_history' : list_chat_history }
    '''
    result = mySession.query(Chat.room_id).all()
    result1 = mySession.query(Chat.line_user_id).all()
    result2 = mySession.query(Chat.line_user_text).all()
    result3 = mySession.query(Chat.web_cov_text).all()
    result4 = mySession.query(Chat.time).all()
    
    result = { 'room_id' : result , 'line_user_id' : result1, 'line_user_text' : result2, 'web_cov_text' : result3, 'time' : result4}

    return result 

#里民資訊
@app.route("/limin_information")
def limin_information():
    list_limin_information = []
    '''与数据库建立链接'''
    engine = create_engine("mysql+pymysql://root:qd513020@localhost:3306/agent",echo=True)

    # 创建会话
    session = sessionmaker(engine)
    mySession = session()



    for name, birthday, phone_number,address, tag in mySession.query(Limin.name, Limin.birthday, Limin.phone_number, Limin.address, Limin.tag):
        print(name, birthday, phone_number, address, tag)
        list_limin_information.append(name)
        list_limin_information.append(birthday)
        list_limin_information.append(phone_number)
        list_limin_information.append(address)
        list_limin_information.append(tag)
        #print(list_chat_history)
        result = { 'limin_information' : list_limin_information }
    #print(result)

    #result = json.dumps(result)
    #print(result)
    #print(result['limin_information'])
    return result 


#里長ID搜尋對應的里民ID
@app.route("/chief_id_find_user_id/<chief_id>")
def chief_id_find_user_id(chief_id):
    list_line_user_id = []
    '''与数据库建立链接'''
    engine = create_engine("mysql+pymysql://root:qd513020@localhost:3306/agent",echo=True)

    # 创建会话
    session = sessionmaker(engine)
    mySession = session()

    for line_user_id in mySession.query(Users.line_user_id).\
                filter_by(chief_id=chief_id):
        print(line_user_id)
        list_line_user_id.append(line_user_id)

    result = { chief_id : list_line_user_id }
    #print(result)
    return result 
    
#里長ID搜尋對應的里民資料
@app.route("/chief_id_find_user_profile/<chief_id>")
def chief_id_find_user_profile(chief_id):
    list_line_user_name = []
    list_line_picture_url = []
    list_line_status_message = []
    '''与数据库建立链接'''
    engine = create_engine("mysql+pymysql://root:qd513020@localhost:3306/agent",echo=True)

    # 创建会话
    session = sessionmaker(engine)
    mySession = session()

    '''
    for chief_id==Kaohsiung , line_user_id, line_user_name in mySession.query(Users.chief_id, Users.line_user_id, Users.line_user_name):
        print(chief_id, line_user_id, line_user_name)
    '''
    for line_user_name, line_picture_url, line_status_message in mySession.query(Users.line_user_name, Users.line_picture_url, Users.line_status_message).\
                filter_by(chief_id=chief_id):
        print(line_user_name, line_picture_url, line_status_message)
        list_line_user_name.append(line_user_name)
        list_line_picture_url.append(line_picture_url)
        list_line_status_message.append(line_status_message)

    #result = { 'line_user_name' : list_line_user_name[0] , 'line_picture_url' : list_line_picture_url[0], 'line_status_message' : list_line_status_message[0]}
    result = { 'line_user_name' : list_line_user_name , 'line_picture_url' : list_line_picture_url, 'line_status_message' : list_line_status_message}
    #print(result)
    return result 

#LINE_USER_ID搜尋對應的LINE用戶資料
@app.route("/user_id_find_user_profile/<line_user_id>")
def user_id_find_user_profile(line_user_id):
    list_line_user_profile = []
    '''与数据库建立链接'''
    engine = create_engine("mysql+pymysql://root:qd513020@localhost:3306/agent",echo=True)

    # 创建会话
    session = sessionmaker(engine)
    mySession = session()

    '''
    for chief_id==Kaohsiung , line_user_id, line_user_name in mySession.query(Users.chief_id, Users.line_user_id, Users.line_user_name):
        print(chief_id, line_user_id, line_user_name)
    '''
    for line_user_name, line_picture_url, line_status_message in mySession.query(Users.line_user_name, Users.line_picture_url, Users.line_status_message).\
                filter_by(line_user_id=line_user_id):
        print(line_user_name, line_picture_url, line_status_message)
        list_line_user_profile.append(line_user_name)
        list_line_user_profile.append(line_picture_url)
        list_line_user_profile.append(line_status_message)
    result = { line_user_id : list_line_user_profile }
    #print(result)
    return result 



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 1004))
    app.run(host='0.0.0.0', port=port,ssl_context=('ca.crt', 'private.key'))