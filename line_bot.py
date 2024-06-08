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
    global control_Device,control_ID,control_Status
    global funtion_num,device_num,status,Device
    global FAN_NUM,NP_FAN_NUM,WATER_NUM,SPRAY_NUM,NUTRIEN_NUM,SHADOW_NUM,SKY_NUM,WINCH_NUM
    LUCAO=["http://yuanmqtt.ddns.net:3650/ui/#!/1?socketid=I_OPwrXcvYvhZXqAAAAB","https://i.imgur.com/qULjBtM.jpg"]
    global img_url,web_url
    
    #宣告選單物件
    
   
    
    fan_menu={ "type": "bubble","header": { "type": "box","layout": "vertical","contents": []},"hero": {"type": "image","url": "https://i.imgur.com/pbNSQiR.png","margin": "xs","gravity": "top"},"body": {"type": "box","layout": "horizontal","contents": [{"type": "text","text": "循環風扇","size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": [{"type": "button","action": {"type": "message","label": "ON","text": "開循環風扇"}},{"type": "button","action": {"type": "message","label": "OFF","text": "關循環風扇"}}]}}
    np_fan_menu={"type": "bubble","header": {"type": "box","layout": "vertical","contents": []},"hero": {"type": "image","url": "https://i.imgur.com/NZufpX3.png"},"body": {"type": "box","layout": "vertical","contents": [{"type": "text","text": "負壓風扇","size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": [{"type": "button","action": {	"type": "message",	"label": "ON",	"text": "開負壓風扇"}},{"type": "button","action": {	"type": "message",	"label": "OFF",	"text": "關負壓風扇"}}]}}
    water_menu={"type": "bubble","header": {"type": "box","layout": "vertical","contents": []},"hero": {"type": "image","url": "https://i.imgur.com/oZVK6F5.png"},"body": {"type": "box","layout": "vertical","contents": [{"type": "text","text": "噴霧馬達","size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": [{"type": "button","action": {"type": "message","text": "開噴霧馬達","label": "ON"}},{"type": "button","action": {"type": "message","label": "OFF","text": "關噴霧馬達"}}]}}
    spray_menu={"type": "bubble","header": {"type": "box","layout": "vertical","contents": []},"hero": {"type": "image","url": "https://i.imgur.com/usdiwDV.png"},"body": {"type": "box","layout": "vertical","contents": [{"type": "text","text": "噴藥馬達","size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": [{"type": "button","action": {"type": "message","text": "開噴藥馬達","label": "ON"}},{"type": "button","action": {"type": "message","label": "OFF","text": "關噴藥馬達"}}]}}
    nuirten_menu={"type": "bubble","header": {"type": "box","layout": "vertical","contents": []},"hero": {"type": "image","url": "https://i.imgur.com/iQ2QaAi.png"},"body": {"type": "box","layout": "vertical","contents": [{"type": "text","text": "養液馬達","size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": [{"type": "button","action": {"type": "message","text": "開養液馬達","label": "ON"}},{"type": "button","action": {"type": "message","label": "OFF","text": "關養液馬達"}}]}}
    shadow_menu={"type": "bubble","header": {"type": "box","layout": "vertical","contents": []},"hero": {"type": "image","url": "https://i.imgur.com/soE2Uvk.png"},"body": {"type": "box","layout": "vertical","contents": [{"type": "text","text": "遮陰控制","size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": [{"type": "button","action": {"type": "message","text": "開遮陰","label": "OPEN"}},{"type": "button","action": {"type": "message","label": "STOP","text": "停遮陰"}},{"type": "button","action": {"type": "message","label": "CLOSE","text": "關遮陰"}}]}}
    winch_menu={"type": "bubble","header": {"type": "box","layout": "vertical","contents": []},"hero": {"type": "image","url": "https://i.imgur.com/8SIOY1l.png"},"body": {"type": "box","layout": "vertical","contents": [{"type": "text","text": "捲揚控制","size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": [{"type": "button","action": {"type": "message","text": "開捲揚","label": "OPEN"}},{"type": "button","action": {"type": "message","label": "STOP","text": "停捲揚"}},{"type": "button","action": {"type": "message","label": "CLOSE","text": "關捲揚"}}]}}
    sky_menu={"type": "bubble","header": {"type": "box","layout": "vertical","contents": []},"hero": {"type": "image","url": "https://i.imgur.com/KYlH7vu.png"},"body": {"type": "box","layout": "vertical","contents": [{"type": "text","text": "天窗控制","size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": [{"type": "button","action": {"type": "message","text": "開天窗","label": "OPEN"}},{"type": "button","action": {"type": "message","label": "STOP","text": "停天窗"}},{"type": "button","action": {"type": "message","label": "CLOSE","text": "關天窗"}}]}}
    #選單容器
    contents=[]
    
    response=requests.get('http://yuanmqtt.ddns.net:3650/getuser')#向SQL中提取所有ID資料
    if response.status_code == 200 :#如果連線成功
        ID_LIST=json.loads(response.text)#將SQL資料寫入陣列
        num=len(ID_LIST)#讀取陣列大小
        for i in range(num):#執行for迴圈,比對當目前使用者ID是否在資料庫中
            if ID_LIST[i]['LINE_ID'] == event.source.user_id:#若使用者ID存在
                control_ID=ID_LIST[i]['SITE_ID']#取得使用者所屬場域代號，並結束迴圈
                #print(control_ID)
                break
    if control_ID=='YUAN':
        img_url=LUCAO[1]
        web_url=LUCAO[0]
    special_menu={ "type": "bubble","header": { "type": "box","layout": "vertical","contents": []},"hero": {"type": "image","url": img_url,"margin": "xs","gravity": "top"},"body": {"type": "box","layout": "horizontal","contents": [{"type": "text","text": "專屬功能","size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": [{"type": "button","action": {"type": "uri","label": "開啟介面","uri": web_url}}]}}
    
    

    for i in event.message.text:#LINE BOT接收的資料
        message_get += i
    #print(message_get)
    #if message_get == "農改場" :#當使用者輸入"報到"時
    #    FlexMessage = json.load(open('layout/special.json','r',encoding='utf-8'))
    #    line_bot_api.reply_message( event.reply_token, FlexSendMessage("專屬功能",FlexMessage))
    
    
    if message_get == "報到" :#當使用者輸入"報到"時
        UserId = event.source.user_id#取得目前使用者的ID
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="您的ID為"+UserId))#回推訊息給使用者，回推內容為ID
    
    if message_get =="聯絡客服":#當使用者輸入"聯絡客服"時
        #回推訊息給使用者，回推內容為客服連結
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="您好，加入客服中心，回報問題後會有專人為您服務 \n連結:https://lin.ee/hxeuVAO"))

    if control_ID != "null" :#如果有對應的LINE_ID
        if message_get =="控制選單":#如果點擊的按鈕是
           
            response=requests.get('http://yuanmqtt.ddns.net:3650/getStage')#向SQL中提取所有的場域資料
            if response.status_code == 200 :#若連線成功
                Stage_Device=json.loads(response.text)#將SQL資料寫入陣列
                print(response.text)
                num=len(Stage_Device)#讀取陣列大小
                for i in range(num):#執行for迴圈，比對當目前場域代號是否在資料庫中
                    if Stage_Device[i]["SITE_ID"] == control_ID:#若場域代號存在
                        funtion_num = Stage_Device[i]["Funtion_NUM"]#取得場域可控設備種類(功能代號)
                        device_num = Stage_Device[i]["Device_NUM"]#取得場域可控各設備數量(設備數量)
                        break#結束迴圈
                #print(funtion_num)
                #print(device_num)
            #funtion_num_tobin=bin(funtion_num)#功能代號值轉成2進位
            funtion_num_tobin='{:012b}'.format(funtion_num)
            funtion_list=list(funtion_num_tobin)#將功能代號拆分進陣列中
            #print(funtion_list)
            device_list=list(device_num)#將設備數量拆分進陣列中
            #print(device_list)
            
            #將對應設備數量填入變數
            FAN_NUM=device_list[0]
            NP_FAN_NUM=device_list[1]
            WATER_NUM=device_list[2]
            SPRAY_NUM=device_list[3]
            NUTRIEN_NUM=device_list[4]
            SHADOW_NUM=device_list[5]
            WINCH_NUM=device_list[6]
            SKY_NUM=device_list[7]
            
            #若對應的功能代號=1時 將選單物件填入選單容器中
            #if funtion_list[2] == '1':
            #	contents.append(special_menu)
            
            
            
            
           

            if funtion_list[3] == '1':#風扇
                contents.append(fan_menu)
            if funtion_list[4] == '1':#負壓
                contents.append(np_fan_menu)
            if funtion_list[5] == '1':#噴霧
                contents.append(water_menu)
            if funtion_list[6] == '1':#噴藥
                contents.append(spray_menu)
            if funtion_list[7] == '1':#養液
                contents.append(nuirten_menu)
            if funtion_list[8] == '1':#遮陰
                contents.append(shadow_menu)
            if funtion_list[9] == '1':#捲揚
                contents.append(winch_menu)
            if funtion_list[10] == '1':#天窗
                contents.append(sky_menu)
            if funtion_list[11]=='1':
                contents.append(special_menu)
            
            
            #更大的選單容器
            content = {"type": "carousel"}
            content.update({"contents": contents}) #將選單容器放進更大的容器中
            message=FlexSendMessage(alt_text='控制選單',contents=content) #LINE_BOT包裝
            line_bot_api.reply_message( event.reply_token, message) #將LINE_BOT包裝 推送給使用者
            
        
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
            if FAN_NUM != '0' :
                control_Device="FAN"
                Device="循環風扇"
                FlexMessage = json.load(open('layout/FAN/FlexMessage_FAN_'+FAN_NUM+'.json','r',encoding='utf-8'))
                line_bot_api.reply_message( event.reply_token, FlexSendMessage("循環風扇",FlexMessage))

        elif "負壓風扇" in message_get :
            if NP_FAN_NUM != '0' :
                control_Device="NP_FAN"
                Device="負壓風扇"
                FlexMessage = json.load(open('layout/NP_FAN/FlexMessage_NP_FAN_'+NP_FAN_NUM+'.json','r',encoding='utf-8'))
                line_bot_api.reply_message( event.reply_token, FlexSendMessage("負壓風扇",FlexMessage))
        elif "噴霧馬達" in message_get :
            if WATER_NUM != '0':
                control_Device="WATER"
                Device="噴霧馬達"
                FlexMessage = json.load(open('layout/WATER/FlexMessage_WATER_'+WATER_NUM+'.json','r',encoding='utf-8'))
                line_bot_api.reply_message( event.reply_token, FlexSendMessage("噴霧馬達",FlexMessage))
        elif "養液馬達" in message_get :
            if NUTRIEN_NUM != '0' :
                control_Device="NUTRIEN"
                Device="養液馬達"
                FlexMessage = json.load(open('layout/N_S/FlexMessage_N_S_'+NUTRIEN_NUM+'.json','r',encoding='utf-8'))
                line_bot_api.reply_message( event.reply_token, FlexSendMessage("養液供應",FlexMessage))
        elif "噴藥馬達" in message_get :
            if SPRAY_NUM != '0' :
                control_Device="SPRAY"
                Device="噴藥馬達"
                FlexMessage = json.load(open('layout/SPRAY/FlexMessage_SPRAY_'+SPRAY_NUM+'.json','r',encoding='utf-8'))
                line_bot_api.reply_message( event.reply_token, FlexSendMessage("噴藥馬達",FlexMessage))
        elif "天窗" in message_get :
            if SKY_NUM != '0' :
                control_Device="SKY"
                Device="天窗"
                FlexMessage = json.load(open('layout/SKY/FlexMessage_SKY_'+SKY_NUM+'.json','r',encoding='utf-8'))
                line_bot_api.reply_message( event.reply_token, FlexSendMessage("天窗控制",FlexMessage))
        elif "遮陰" in message_get :
            if SHADOW_NUM != '0' :
                control_Device="SHADOW"
                Device="遮陰"
                FlexMessage = json.load(open('layout/SHADOW/FlexMessage_SHADOW_'+SHADOW_NUM+'.json','r',encoding='utf-8'))
                line_bot_api.reply_message( event.reply_token, FlexSendMessage("遮陰控制",FlexMessage))
        elif "捲揚" in message_get :
            if WINCH_NUM != '0' :
                control_Device="WINCH"
                Device="捲揚"
                FlexMessage = json.load(open('layout/WINCH/FlexMessage_WINCH_'+WINCH_NUM+'.json','r',encoding='utf-8'))
                line_bot_api.reply_message( event.reply_token, FlexSendMessage("捲揚控制",FlexMessage))
    else : #如果沒有
        line_bot_api.reply_message(
        event.reply_token,
            TextSendMessage(text="您尚未擁有控制權，請在對話框輸入[報到]!")
        )
        

#使用者選擇設備編號開關後 進行後台運作
@handler.add(PostbackEvent)
def handle_postback(event):
#這裡放你要做的事情


    ts = event.postback.data
    if ts!= "richmenu-changed-to-a" and ts!= "richmenu-changed-to-b":
        #test(control_ID,FAN,ts)
        print(ts+","+control_Device+","+control_ID+","+control_Status)
        response = requests.get(url="http://yuanmqtt.ddns.net:3650/"+control_Device+"?Device="+control_Device+"&NUM="+ts+"&Status="+control_Status+"&userID="+control_ID)
        print(response.status_code)
        print(response.text)
        if response.status_code==200:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=Device+ts+"號 "+status)
                )




if __name__ == "__main__":
    app.run()
