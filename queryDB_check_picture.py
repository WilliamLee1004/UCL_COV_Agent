#coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric
from lichangbo_createDB import engine,Chat,Users
from  sqlalchemy.orm import sessionmaker

import requests
import json


'''与数据库建立链接'''
engine = create_engine("mysql+pymysql://root:qd513020@localhost:3306/agent",echo=True)

# 创建会话
session = sessionmaker(engine)
mySession = session()

# 查询结果集
#result = mySession.query(Users).all()
#print(result[0])

#取出db中所有的line_user_id
result = mySession.query(Users.line_user_id).all()
#print總共有幾筆line_user_id
print(mySession.query(Users.line_user_id).count())

#將list轉為dict並給予key值
dict_result = dict(list(enumerate(result, start=1)))
#取出value轉為字串
#str_user_id = str(dict_result['2'])
#去掉多餘符號整理成乾淨的ID
#print(str_user_id[2:-3])
#從第一筆line_user_id開始檢查使用者頭像
for i in range(1,mySession.query(Users.line_user_id).count() +1):
    str_user_id = str(dict_result[i])
    print(str_user_id[2:-3])

    url = 'https://api.line.me/v2/bot/profile/%s'%(str_user_id[2:-3])
    token = 'Qw41For/uMNtw6fWwFF//qbHp7ThrQCckmZP47PtUyKk8Bk7jQl1gXF4mjfUXQrQB2smf7Dx1ZqeZv6Ggtwyta6zhe6Nzn+EPtkiOrv992qJoayHtFn5ORyB9GEXIdVGLxqu+ISyZYCk/6+45Qv5xAdB04t89/1O/w1cDnyilFU='

    r = requests.get(url, headers={'Authorization': 'Bearer ' + token})
    #print(r.text)
    user_profile = r.text
    user_profile = json.loads(user_profile)
    print(user_profile['pictureUrl'])
    mySession.query(Users).filter(Users.line_user_id == str_user_id[2:-3]).update({"line_picture_url":user_profile['pictureUrl']})
    mySession.commit()