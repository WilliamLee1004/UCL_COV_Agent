#以版本12為基礎完成圖文選單基本服務和第一層流程

import os
import json
import websocket
import requests


from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi('Qw41For/uMNtw6fWwFF//qbHp7ThrQCckmZP47PtUyKk8Bk7jQl1gXF4mjfUXQrQB2smf7Dx1ZqeZv6Ggtwyta6zhe6Nzn+EPtkiOrv992qJoayHtFn5ORyB9GEXIdVGLxqu+ISyZYCk/6+45Qv5xAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4d62865722f575922dc2a337cf76f55b')
to = "U81cef0c79acd31e21aaaf8e7109d3ed0"

global reply
room_type = 0

try:
    import thread
except ImportError:
    import _thread as thread

import time
#收發訊息
def on_message(ws, message):
    from sqlalchemy.orm.session import sessionmaker
    from lichangbo_createDB import engine,Chat
    print(ws)
    print(message)
    reply = message
    reply = json.loads(reply)
    print(reply)
    print(reply['msg'])
    print('===')
    to = reply['roomid']
    reply = reply['msg']
    
    #存放聊天紀錄
    chat = Chat()
    chat.room_id = user_id
    chat.line_user_id = user_id
    chat.line_user_text = msg
    chat.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #chat.web_cov_text = reply
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    session.add(chat)
    session.flush()
    session.commit()
    if reply !=msg :    #判斷reply為里長回復msg為里民訊息
        line_bot_api.push_message(to, TextSendMessage(text=reply))
        
        #存放聊天紀錄
        chat = Chat()
        chat.room_id = user_id
        chat.line_user_id = user_id
        #chat.line_user_text = msg
        chat.web_cov_text = reply
        chat.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()
        session.add(chat)
        session.flush()
        session.commit()


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("連線中斷")

def on_open(ws):
    print("已經ws連線成功!!!")
    
    Agent = '{"type":"join","roomid":"%s","userid":"%s"}'%(user_id, user_id)
    ws.send(Agent)

    message = '{"type":"text","roomid":"%s","userid":"%s", "message":"%s"}'%(user_id, user_id, user_text)
    ws.send(message)
    print("連接成功")
    
def connect_websocket():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://chatbot-rtcserver.54ucl.com:3000",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    
    ws.on_open = on_open
    ws.run_forever()

def extract_requset_data(data):
    dict1 = data
    list1 = dict1['events']
    dict2 = list1.pop()
    dict3 = dict2['message']
    formate_data = dict3
    return formate_data


def extract_LContext_ENGINE_data(data):
    data.pop('type')
    data.pop('id')
    #tax_ID_number = data['text']
    Context_json = {'LContext': data['text']}
    ENGINE_data = json.dumps(Context_json)
    return ENGINE_data

def get_user_profile(user_id):
    url = 'https://api.line.me/v2/bot/profile/%s'%(user_id)
    token = 'Qw41For/uMNtw6fWwFF//qbHp7ThrQCckmZP47PtUyKk8Bk7jQl1gXF4mjfUXQrQB2smf7Dx1ZqeZv6Ggtwyta6zhe6Nzn+EPtkiOrv992qJoayHtFn5ORyB9GEXIdVGLxqu+ISyZYCk/6+45Qv5xAdB04t89/1O/w1cDnyilFU='

    r = requests.get(url, headers={'Authorization': 'Bearer ' + token})
    print(r.text)
    user_profile = r.text
    user_profile = json.loads(user_profile)
    print(type(user_profile))
    print(user_profile['displayName'])

    from sqlalchemy.orm.session import sessionmaker
    from lichangbo_createDB import engine,Users
    users = Users()
    users.chief_id = 'Kaohsiung'
    users.role = 'Kaohsiung'
    users.line_user_id = user_profile['userId']
    users.line_user_name = user_profile['displayName']
    users.line_picture_url = user_profile['pictureUrl']
    users.line_status_message = user_profile['statusMessage']
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    session.add(users)
    session.flush()
    session.commit()




# 監聽所有來自 /callback 的 Post Request


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    data = json.loads(body)
    print("Request data_format_dict: {}".format(data))

    # 提取request中需要存入DB的資料
    LContext_data = extract_requset_data(data)   # func extract_requset_data
    print(LContext_data['text'])
    global msg
    msg = LContext_data['text']
    

    #建立連線
    #connect_websocket()

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    global user_id
    user_id = event.source.user_id
    global user_text 
    user_text = event.message.text
    print("user_id =", user_id)
    print("user_text =", user_text)
    
    #rich_menu處理
    #text = event.message.text
    if user_text == '最新消息':
        from sqlalchemy import create_engine
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy import Column, Integer, String, Numeric
        from lichangbo_createDB import engine,Chat,Users,News,Service
        from  sqlalchemy.orm import sessionmaker

        import requests
        import json

        list_latest_news = []
        '''与数据库建立链接'''
        engine = create_engine("mysql+pymysql://root:qd513020@localhost:3306/agent",echo=True)

        # 创建会话
        session = sessionmaker(engine)
        mySession = session()



        for title, introduction, link, date, district in mySession.query(News.title, News.introduction, News.link, News.date, News.district):
            print(title, introduction, link, date, district)
            list_latest_news.append(title)
            list_latest_news.append(introduction)
            list_latest_news.append(link)
            list_latest_news.append(date)
            list_latest_news.append(district)
            #print(list_latest_news)
            result = { 'latest_news' : list_latest_news }
        #print(result)

        #result = json.dumps(result)
        print(result)
        print(result['latest_news'])
        print(type(result))
        message = TextSendMessage(text=str(list_latest_news[0]+ ' :\n' + list_latest_news[1] +'\n連結 : '+ list_latest_news[2]))
        print(message)
        line_bot_api.reply_message(event.reply_token, message)
    elif user_text == '里區服務':
        from sqlalchemy import create_engine
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy import Column, Integer, String, Numeric
        from lichangbo_createDB import engine,Chat,Users,News,Service
        from  sqlalchemy.orm import sessionmaker

        import requests
        import json

        list_district_service = []
        '''与数据库建立链接'''
        engine = create_engine("mysql+pymysql://root:qd513020@localhost:3306/agent",echo=True)

        # 创建会话
        session = sessionmaker(engine)
        mySession = session()



        for district, introduction in mySession.query(Service.district, Service.introduction):
            print(district, introduction)
            list_district_service.append(district)
            list_district_service.append(introduction)
            
            #print(list_district_service)
            result = { 'district_service' : list_district_service }
        #print(result)

        #result = json.dumps(result)
        print(result)
        print(result['district_service'])
        print(type(result))
        message = TextSendMessage(text=str(list_district_service[1]))
        print(message)
        line_bot_api.reply_message(event.reply_token, message)
    elif user_text == '資料查詢':
        import requests
        import json
        url = "https://chatbot-rtcserver.54ucl.com:7810/Process/Message"
        projectId = "covchatbot-evwylu"

        Context_json = json.dumps(
            {"projectId": projectId,"msg": user_text})
        result = requests.post(url, data=Context_json)
        #print(result.text)
        reply = result.text
        reply = json.loads(reply)
        #print(reply['Rcontext']['options'][1])
        QuickReply_text_message = TextSendMessage(
            text='請問想詢問的服務?',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label=reply['Rcontext']['options'][0], text=reply['Rcontext']['options'][0]),
                    ),
                    QuickReplyButton(
                        action=MessageAction(label=reply['Rcontext']['options'][1], text=reply['Rcontext']['options'][1]),
                    ),
                    QuickReplyButton(
                        action=MessageAction(label=reply['Rcontext']['options'][2], text=reply['Rcontext']['options'][2]),
                    ),
                    QuickReplyButton(
                        action=MessageAction(label=reply['Rcontext']['options'][3], text=reply['Rcontext']['options'][3]),
                    ),
                    QuickReplyButton(
                        action=MessageAction(label=reply['Rcontext']['options'][4], text=reply['Rcontext']['options'][4]),
                    ),
                    QuickReplyButton(
                        action=MessageAction(label=reply['Rcontext']['options'][5], text=reply['Rcontext']['options'][5]),
                    ),
                    QuickReplyButton(
                        action=MessageAction(label=reply['Rcontext']['options'][6], text=reply['Rcontext']['options'][6]),
                    ),
                    QuickReplyButton(
                        action=MessageAction(label=reply['Rcontext']['options'][7], text=reply['Rcontext']['options'][7]),
                    ),
                    QuickReplyButton(
                        action=MessageAction(label=reply['Rcontext']['options'][8], text=reply['Rcontext']['options'][8]),
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, QuickReply_text_message)
        
        #line_bot_api.push_message(user_id, QuickReply_text_message)
        
    
    elif user_text == '1.低收入戶':
        import requests
        import json
        url = "https://chatbot-rtcserver.54ucl.com:7810/Process/Message"
        projectId = "covchatbot-evwylu"

        Context_json = json.dumps(
            {"projectId": projectId,"msg": user_text})
        result = requests.post(url, data=Context_json)
        #print(result.text)
        reply = result.text
        reply = json.loads(reply)
        #print(reply['Rcontext']['options'][1])
        QuickReply_text_message = TextSendMessage(
            text='請選擇',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label=reply['Rcontext']['options'][0], text=reply['Rcontext']['options'][0]),
                    ),
                    QuickReplyButton(
                        action=MessageAction(label=reply['Rcontext']['options'][1], text=reply['Rcontext']['options'][1]),
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, QuickReply_text_message)

    elif user_text == '1.應備文件':
        import requests
        import json
        url = "https://chatbot-rtcserver.54ucl.com:7810/Process/Message"
        projectId = "covchatbot-evwylu"

        Context_json = json.dumps(
            {"projectId": projectId,"msg": user_text})
        result = requests.post(url, data=Context_json)
        #print(result.text)
        reply = result.text
        reply = json.loads(reply)
        print(reply['Rcontext']['content'])
        message = TextSendMessage(text=reply['Rcontext']['content'])
        line_bot_api.reply_message(event.reply_token, message)

    elif user_text == '2.服務單位、洽詢電話':
        import requests
        import json
        url = "https://chatbot-rtcserver.54ucl.com:7810/Process/Message"
        projectId = "covchatbot-evwylu"

        Context_json = json.dumps(
            {"projectId": projectId,"msg": user_text})
        result = requests.post(url, data=Context_json)
        #print(result.text)
        reply = result.text
        reply = json.loads(reply)
        print(reply['Rcontext']['content'])
        message = TextSendMessage(text=reply['Rcontext']['content'])
        line_bot_api.reply_message(event.reply_token, message)

    elif user_text == '事件通報':
        
        import requests
        import json
        url = "https://chatbot-rtcserver.54ucl.com:7810/Process/Message"
        projectId = "covchatbot-evwylu"

        Context_json = json.dumps(
            {"projectId": projectId,"msg": user_text})
        result = requests.post(url, data=Context_json)
        #print(result.text)
        reply = result.text
        reply = json.loads(reply)
        #print(reply['Rcontext']['options'][1])
        

        
        Confirm_text_message = TemplateSendMessage(
            alt_text= '確認樣板',
            
            template = ConfirmTemplate(
                text = '請選擇',
                actions=[
                    MessageTemplateAction(
                        label = reply['Rcontext']['options'][0],
                        text = reply['Rcontext']['options'][0]
                    ),
                    MessageTemplateAction(
                        label = reply['Rcontext']['options'][1],
                        text = reply['Rcontext']['options'][1]
                    )
                ]
            )
            
        )

        line_bot_api.reply_message(event.reply_token, Confirm_text_message)
    
    elif user_text == '2.申請案件':
        import requests
        import json
        url = "https://chatbot-rtcserver.54ucl.com:7810/Process/Message"
        projectId = "covchatbot-evwylu"

        Context_json = json.dumps(
            {"projectId": projectId,"msg": user_text})
        result = requests.post(url, data=Context_json)
        #print(result.text)
        reply = result.text
        reply = json.loads(reply)
        message = TextSendMessage(text=reply['Rcontext']['content'])
    else:
        #建立連線
        connect_websocket()
    
    


@handler.add(FollowEvent)
def handle_follow(event):
    print('follow')
    user_id = event.source.user_id
    print(user_id)
    get_user_profile(user_id)

@handler.add(UnfollowEvent)
def handle_unfollow(event):
    print('unfollow')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port,ssl_context=('ca.crt', 'private.key'))
    
