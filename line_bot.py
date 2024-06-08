from __future__ import unicode_literals
import os
import json
import requests
import time
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,FlexSendMessage,PostbackEvent

import configparser

import random

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        #print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 建立選單
@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    message_get = ''
    global control_Device
    global control_ID
    global control_Status
    global status
    global Device
    global name
    
    response=requests.get('http://yuanmqtt.ddns.net:1886/sql')
    if response.status_code == 200 :
        ID_LIST=json.loads(response.text)
        num=len(ID_LIST)
        for i in range(num):
            if ID_LIST[i]["LINE_ID"] == event.source.user_id:
                control_ID=ID_LIST[i]["SITE_ID"]
                name=ID_LIST[i]["name"]
                print(control_ID)
                break

    for i in event.message.text:
        message_get += i
    #print(message_get)
    if message_get == "報到" :
        UserId = event.source.user_id
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="您的ID為"+UserId)
        )

    if control_ID != "null" :#如果有對應的LINE_ID


        
        if message_get =="控制選單":
        
        

            A='255'
            FlexMessage = json.load(open('layout/ALL_MENU/FlexMessage_control_'+A+'.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("控制選單",FlexMessage))


            
        elif message_get =="聯絡客服":
            line_bot_api.reply_message(
            event.reply_token,
                TextSendMessage(text="您好，加入客服中心，回報問題後會有專人為您服務 \n連結:https://lin.ee/hxeuVAO")
            )
        if "開" in message_get:
            control_Status="ON"
            status="開"
        elif "關" in message_get:
            control_Status="OFF"
            status="關"
        elif "停" in message_get:
            control_Status="STOP"
            status="停"

        if "循環風扇" in message_get :
            control_Device="FAN"
            Device="循環風扇"
            FlexMessage = json.load(open('layout/FAN/FlexMessage_FAN_3.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("循環風扇",FlexMessage))
        elif "負壓風扇" in message_get :
            control_Device="NP_FAN"
            Device="負壓風扇"
            FlexMessage = json.load(open('layout/NP_FAN/FlexMessage_NP_FAN_3.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("負壓風扇",FlexMessage))
        elif "噴霧馬達" in message_get :
            control_Device="WATER"
            Device="噴霧馬達"
            FlexMessage = json.load(open('layout/WATER/FlexMessage_WATER_3.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("噴霧馬達",FlexMessage))
        elif "養液馬達" in message_get :
            control_Device="nutrien"
            Device="養液馬達"
            FlexMessage = json.load(open('layout/N_S/FlexMessage_N_S_3.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("養液供應",FlexMessage))
        elif "噴藥馬達" in message_get :
            control_Device="SPRAY"
            Device="噴藥馬達"
            FlexMessage = json.load(open('layout/SPRAY/FlexMessage_SPRAY_3.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("噴藥馬達",FlexMessage))
        elif "天窗" in message_get :
            control_Device="SKY"
            Device="天窗"
            FlexMessage = json.load(open('layout/SKY/FlexMessage_SKY_3.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("天窗控制",FlexMessage))
        elif "遮陰" in message_get :
            control_Device="SHADOW"
            Device="遮陰"
            FlexMessage = json.load(open('layout/SHADOW/FlexMessage_SHADOW_3.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("遮陰控制",FlexMessage))
        elif "捲揚" in message_get :
            control_Device="WINCH"
            Device="捲揚"
            FlexMessage = json.load(open('layout/WINCH/FlexMessage_WINCH_3.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("捲揚控制",FlexMessage))
    else : #如果沒有
        line_bot_api.reply_message(
        event.reply_token,
            TextSendMessage(text="您尚未擁有控制權，請在對話框輸入[報到]!")
        )


@handler.add(PostbackEvent)
def handle_postback(event):
    ts = event.postback.data
    if ts!= "richmenu-changed-to-a" and ts!= "richmenu-changed-to-b":
        #test(control_ID,FAN,ts)
        print(ts+","+control_Device+","+control_ID+","+control_Status)
        response = requests.get(url="http://yuanmqtt.ddns.net:1886/"+control_Device+"?Device="+control_Device+"&NUM="+ts+"&Status="+control_Status+"&userID="+control_ID)
        print(response.status_code)
        print(response.text)
        if response.status_code==200:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=Device+ts+"號 "+status)
                )



if __name__ == "__main__":
    app.run()