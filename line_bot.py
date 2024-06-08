from __future__ import unicode_literals
import os
import json
import requests
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

    for i in event.message.text:
        message_get += i
    #print(message_get)

    

        
        
        
    if message_get =="控制選單":
        FlexMessage = json.load(open('FlexMessage_control.json','r',encoding='utf-8'))
        line_bot_api.reply_message( event.reply_token, FlexSendMessage("控制選單",FlexMessage))
        if event.source.user_id == "U8886a35f392fc9a1fecad167c6ffd484" or event.source.user_id == "U553115716cb408b9c01266537f1bff1d":
            control_ID="yuan"
            
    elif message_get =="聯絡客服":
        line_bot_api.reply_message(
        event.reply_token,
            TextSendMessage(text="您好，加入客服中心，回報問題後會有專人為您服務 \n連結:https://lin.ee/hxeuVAO")
        )
            
    else :        
        if message_get =="開循環風扇":
            FlexMessage = json.load(open('FlexMessage.json','r',encoding='utf-8'))
            control_Status="ON"
            control_Device="FAN"
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("循環風扇",FlexMessage))
        elif message_get=="關循環風扇":
            control_Status="OFF"
            control_Device="FAN"
            FlexMessage = json.load(open('FlexMessage.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("循環風扇",FlexMessage))
        if message_get =="開負壓風扇":
            control_Status="ON"
            control_Device="NP_FAN"
            FlexMessage = json.load(open('FlexMessage_NP_FAN.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("負壓風扇",FlexMessage))
        elif message_get=="關負壓風扇":
            control_Status="OFF"
            control_Device="NP_FAN"
            FlexMessage = json.load(open('FlexMessage_NP_FAN.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("負壓風扇",FlexMessage))
        if message_get =="開噴霧馬達":
            control_Status="ON"
            control_Device="WATER"
            FlexMessage = json.load(open('FlexMessage_WATER.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("噴霧馬達",FlexMessage))
        elif message_get =="關噴霧馬達":
            control_Status="OFF"
            control_Device="WATER"
            FlexMessage = json.load(open('FlexMessage_WATER.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("噴霧馬達",FlexMessage))

        if message_get =="開養液":
            control_Status="ON"
            control_Device="nutrien"
            FlexMessage = json.load(open('FlexMessage_N_S.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("養液供應",FlexMessage))
        elif message_get =="關養液":
            control_Status="OFF"
            control_Device="nutrien"
            FlexMessage = json.load(open('FlexMessage_N_S.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("養液供應",FlexMessage))


        if message_get =="開噴藥馬達":
            control_Status="ON"
            control_Device="SPPRAY"
            FlexMessage = json.load(open('FlexMessage_SPRAY.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("噴藥馬達",FlexMessage))
        elif message_get =="關噴藥馬達":
            control_Status="OFF"
            control_Device="SPPRAY"
            FlexMessage = json.load(open('FlexMessage_SPRAY.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("噴藥馬達",FlexMessage))



        if message_get =="開天窗":
            FlexMessage = json.load(open('FlexMessage_SKY.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("天窗控制",FlexMessage))
        elif message_get =="關天窗":
            FlexMessage = json.load(open('FlexMessage_SKY.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("天窗控制",FlexMessage))
            
        if message_get =="開遮陰":
            FlexMessage = json.load(open('FlexMessage_SHADOW.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("遮陰控制",FlexMessage))
        elif message_get =="關遮陰":
            FlexMessage = json.load(open('FlexMessage_SHADOW.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("遮陰控制",FlexMessage))

        if message_get =="開捲揚":
            FlexMessage = json.load(open('FlexMessage_WINCH.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("捲揚控制",FlexMessage))
        elif message_get =="關捲揚":
            FlexMessage = json.load(open('FlexMessage_WINCH.json','r',encoding='utf-8'))
            line_bot_api.reply_message( event.reply_token, FlexSendMessage("捲揚控制",FlexMessage))
        
    
        #else:
        #    line_bot_api.reply_message(
        #        event.reply_token,
        #        TextSendMessage(text=message_get)
        #    )

"""else :
        if message_get == "報到" :
            print("取得id :")
            UserId = event.source.user_id
            print(UserId)
            print(" ")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="您的ID為"+UserId)
            )
        else :
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="您尚未擁有控制權，請在對話框輸入[報到]後取得您的ID，並連繫服務人員!")
            )"""
@handler.add(PostbackEvent)
def handle_postback(event):
    ts = event.postback.data
    if ts!= "richmenu-changed-to-a" and ts!= "richmenu-changed-to-b":
        #test(control_ID,FAN,ts)
        
        print(ts+","+control_Device+","+control_ID+","+control_Status)
        if control_Status =="ON" :
            status="開"
        else :
            status="關"
        if control_Device=="FAN" :
            Device="循環風扇"
        elif control_Device=="NP_FAN":
            Device="負壓風扇"
        elif control_Device=="WATER":
            Device="噴霧馬達"
        
        response = requests.get(url="http://yuanmqtt.ddns.net:1886/"+control_Device+"?Device="+control_Device+"&NUM="+ts+"&Status="+control_Status+"&userID="+control_ID)
        print(response.status_code)
        print(response.text)
        if response.status_code==200:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=Device+ts+status)
                )

"""
    line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=ts)
            )
"""


if __name__ == "__main__":
    app.run()