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

import threading

app = Flask(__name__)
stage_ID_list=[]



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
    global funtion_num,device_num,status,Device,stage_num
    global FAN_NUM,NP_FAN_NUM,WATER_NUM,SPRAY_NUM,NUTRIEN_NUM,SHADOW_NUM,SKY_NUM,WINCH_NUM,DI_NUM,LAMP_NUM,MOD_NUM
    global stage_ID_list
    #global img_url,web_url

    
    #宣告選單物件
                
#場域
    #stage_menu={ "type": "bubble","header": { "type": "box","layout": "vertical","contents": []},"body": {"type": "box","layout": "horizontal","contents": [{"type": "text","text": "場域","size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": [{"type": "button","action": {"type": "message","label": "ON","text": "開設備"}},{"type": "button","action": {"type": "message","label": "OFF","text": "關設備"}}]}}
#切換控制
    change_menu={"type": "bubble","header": {"type": "box","layout": "vertical","contents": []},"hero": {"type": "image","url": "https://i.imgur.com/v8jctCY.png"},"body": {"type": "box","layout": "vertical","contents": [{"type": "text","text": "本地遠端切換","size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": []}}
    #循環風扇
    fan_menu={ "type": "bubble","header": { "type": "box","layout": "vertical","contents": []},"hero": {"type": "image","url": "https://i.imgur.com/pbNSQiR.png"},"body": {"type": "box","layout": "horizontal","contents": [{"type": "text","text": "循環風扇","size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": []}}
    #負壓風扇
    np_fan_menu={"type": "bubble" ,"header": {"type": "box","layout": "vertical","contents": []} ,"hero": {"type": "image","url": "https://i.imgur.com/NZufpX3.png"},"body": {"type": "box","layout": "vertical","contents": [{"type": "text","text": "負壓風扇","size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": []}}
    #噴霧迴路
    water_menu={"type": "bubble","header": {"type": "box","layout": "vertical","contents": []},"hero": {"type": "image","url": "https://i.imgur.com/oZVK6F5.png"},"body": {"type": "box","layout": "vertical","contents": [{"type": "text","text": "噴霧迴路","size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": []}}
    #噴藥迴路
    spray_menu={"type": "bubble","header": {"type": "box","layout": "vertical","contents": []},"hero": {"type": "image","url": "https://i.imgur.com/usdiwDV.png"},"body": {"type": "box","layout": "vertical","contents": [{"type": "text","text": "噴藥迴路","size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": []}}
    #微噴迴路
    nuirten_menu={"type": "bubble","header": {"type": "box","layout": "vertical","contents": []},"hero": {"type": "image","url": "https://i.imgur.com/QYu3ynt.png"},"body": {"type": "box","layout": "vertical","contents": [{"type": "text","text": "微噴迴路","size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": []}}
    #滴灌迴路(Drip Irrigation)
    DI_menu={"type": "bubble","header": {"type": "box","layout": "vertical","contents": []},"hero": {"type": "image","url": "https://i.imgur.com/1Z1aeW9.png"},"body": {"type": "box","layout": "vertical","contents": [{"type": "text","text": "滴灌迴路","size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": []}}
    #遮陰
    shadow_menu={"type": "bubble","header": {"type": "box","layout": "vertical","contents": []},"hero": {"type": "image","url": "https://i.imgur.com/soE2Uvk.png"},"body": {"type": "box","layout": "vertical","contents": [{"type": "text","text": "遮陰控制","size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": []}}
    #捲揚
    winch_menu={"type": "bubble","header": {"type": "box","layout": "vertical","contents": []},"hero": {"type": "image","url": "https://i.imgur.com/8SIOY1l.png"},"body": {"type": "box","layout": "vertical","contents": [{"type": "text","text": "捲揚控制","size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": []}}
    #天窗
    sky_menu={"type": "bubble","header": {"type": "box","layout": "vertical","contents": []},"hero": {"type": "image","url": "https://i.imgur.com/KYlH7vu.png"},"body": {"type": "box","layout": "vertical","contents": [{"type": "text","text": "天窗控制","size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": []}}
    #植物燈 
    lamp_menu={"type": "bubble","header": {"type": "box","layout": "vertical","contents": []},"hero": {"type": "image","url": "https://i.imgur.com/u6YJO3L.png"},"body": {"type": "box","layout": "vertical","contents": [{"type": "text","text": "植物燈","size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": []}}
    
   #選單容器
    contents=[]
    for i in event.message.text:#LINE BOT接收的資料
        message_get += i

    if message_get == "報到" :#當使用者輸入"報到"時
        UserId = event.source.user_id#取得目前使用者的ID
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="您的ID為"+UserId))#回推訊息給使用者，回推內容為ID
    
    if message_get =="聯絡客服":#當使用者輸入"聯絡客服"時
        #回推訊息給使用者，回推內容為客服連結
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="您好，加入客服中心，回報問題後會有專人為您服務 \n連結:https://lin.ee/hxeuVAO"))
    if message_get =="查看感測":#當使用者輸入"聯絡客服"時
        #回推訊息給使用者，回推內容為客服連結
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="功能待新增"))
    
    if message_get =="控制選單":#如果點擊的按鈕是
        response=requests.get('http://yuanmqtt.ddns.net:3650/getUser?userID='+event.source.user_id)#向SQL中提取對應ID資料
        if response.status_code == 200 :#如果連線成功
            ID_LIST=json.loads(response.text)#將SQL資料寫入陣列並轉成json
            print (ID_LIST)
            if len(ID_LIST) > 0 :
                control_ID=ID_LIST[0]['SITE_ID']#取得使用者所屬場域代號
                response=requests.get('http://yuanmqtt.ddns.net:3650/getStage?site_ID='+control_ID) #向SQL中提取所有的場域資料
                if response.status_code == 200 :#若連線成功
                    stage_ID_list=[]
                    Stage=json.loads(response.text)#將SQL資料寫入陣列
                    STAGE=Stage[0]['STAGE_NAME']
                    stage_message=STAGE.split(',')
                    num=len(stage_message)
                    for i in range(num):
                        stage_ID=stage_message[i]
                        stage_ID_list.append(stage_ID)
                        #stage_choose="選擇場域"+str(i+1)
                        stage_on="開啟場域"+str(i+1)+"設備"
                        stage_off="關閉場域"+str(i+1)+"設備"
                        stage_stop="停止場域"+str(i+1)+"設備"
                        stage_menu={ "type": "bubble","header": { "type": "box","layout": "vertical","contents": []},"body": {"type": "box","layout": "horizontal","contents": [{"type": "text","text": stage_ID,"size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": [{"type": "button","action": {"type": "message","label": "開啟","text": stage_on}},{"type": "button","action": {"type": "message","label": "停止","text": stage_stop}},{"type": "button","action": {"type": "message","label": "關閉","text": stage_off}}]}}
                        contents.append(stage_menu)
                    content = {"type": "carousel"}
                    content.update({"contents": contents}) #將選單容器放進更大的容器中
                    message=FlexSendMessage(alt_text='控制選單',contents=content) #LINE_BOT包裝
                    line_bot_api.reply_message( event.reply_token, message) #將LINE_BOT包裝 推送給使用者
            else : #如果沒有
                line_bot_api.reply_message(
                event.reply_token,
                    TextSendMessage(text="您尚未擁有控制權，請在對話框輸入[報到]!")
            )

    if "場域" in message_get:
        if "開啟" in message_get:
            control_Status="ON"
            status="開啟"
        elif "關閉" in message_get:
            control_Status="OFF"
            status="關閉"
        elif "停止" in message_get:
            
            status="停止"
            control_Status="STOP"
        stage_num=message_get[4]
        if(stage_num!=None and control_ID!=None):
            response = requests.get(url="http://yuanmqtt.ddns.net:3650/getDevice?site_ID="+control_ID+"&site_NUM="+stage_num)
            #print(response.text)
            if response.status_code == 200 :#若連線成功
                Stage_Device=json.loads(response.text)
                funtion_num = Stage_Device[0]['Funtion_NUM']#取得場域可控設備種類(功能代號)
                device_num = Stage_Device[0]['Device_NUM']#取得場域可控各設備數量(設備數量)
                funtion_num_tobin='{:016b}'.format(funtion_num)
                funtion_list=list(funtion_num_tobin)#將功能代號拆分進陣列中
                device_list=list(device_num)#將設備數量拆分進陣列中
                print (device_list)
                #將對應設備數量填入變數
                MOD_NUM=int(device_list[1])
                FAN_NUM=int(device_list[2])
                NP_FAN_NUM=int(device_list[3])
                WATER_NUM=int(device_list[4])
                SPRAY_NUM=int(device_list[5])
                DI_NUM=int(device_list[6])
                NUTRIEN_NUM=int(device_list[7])
                SHADOW_NUM=int(device_list[8])
                WINCH_NUM=int(device_list[9])
                SKY_NUM=int(device_list[10])
                LAMP_NUM=int(device_list[11])
                
                if status=="開啟" or status=="關閉":
                    print("目前功能有:")

                    if funtion_list[0] == '1':#專屬功能
                        print("專屬")
                        response = requests.get(url="http://yuanmqtt.ddns.net:3650/getSpecial?SITE_ID="+control_ID)
                        if response.status_code==200: 
                            SPECIAL_DATA=json.loads(response.text)
                            print (type(SPECIAL_DATA[0]))
                            img_url=SPECIAL_DATA[0]['img_url']
                            web_url=SPECIAL_DATA[0]['funtion_url']
                            special_menu={ "type": "bubble","header": { "type": "box","layout": "vertical","contents": []},"hero": {"type": "image","url": img_url,"margin": "xs","gravity": "top"},"body": {"type": "box","layout": "horizontal","contents": [{"type": "text","text": "專屬功能","size": "30px","gravity": "top","wrap": False,"weight": "bold","style": "normal","position": "relative","align": "center"}]},"footer": {"type": "box","layout": "vertical","contents": [{"type": "button","action": {"type": "uri","label": "開啟介面","uri": web_url}}]}}
                            contents.append(special_menu)
                    if funtion_list[1] == '1':#手動遠端
                        print("手/自動")
                        change_elementA={"type": "button","action": {"type": "postback","label": "本地控制","data": "{\"SITE_NUM\":\""+stage_num+"\",\"SITE_NAME\":\""+control_ID+"\",\"Device\":\"控制切換\",\"control_Device\":\"MOD\",\"status\":\"本地控制\",\"control_Status\":\"OFF\",\"NUM\":\""+stage_num+"\",\"stage_name\":\""+stage_ID_list[int(stage_num)-1]+"\"}"}}
                        change_elementB={"type": "button","action": {"type": "postback","label": "遠端控制","data": "{\"SITE_NUM\":\""+stage_num+"\",\"SITE_NAME\":\""+control_ID+"\",\"Device\":\"控制切換\",\"control_Device\":\"MOD\",\"status\":\"遠端控制\",\"control_Status\":\"ON\",\"NUM\":\""+stage_num+"\",\"stage_name\":\""+stage_ID_list[int(stage_num)-1]+"\"}"}}
                        change_menu['footer']['contents'].append(change_elementA)
                        change_menu['footer']['contents'].append(change_elementB)
                        contents.append(change_menu)
                    if funtion_list[2] == '1':#風扇
                        print("循環扇")
                        if FAN_NUM <4:
                            fan_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif FAN_NUM < 7 and FAN_NUM >= 4:
                            fan_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            fan_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif FAN_NUM >6 :
                            fan_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            fan_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            fan_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        
                        for i in range(FAN_NUM):
                            fan_element={"type": "button","action": {"type": "postback","label": str(i+1)+"號","data": "{\"SITE_NUM\":\""+stage_num+"\",\"SITE_NAME\":\""+control_ID+"\",\"Device\":\"循環風扇\",\"control_Device\":\"FAN\",\"status\":\""+status+"\",\"control_Status\":\""+control_Status+"\",\"NUM\":\""+str(i+1)+"\",\"control_ID\":\""+control_ID+"\",\"stage_name\":\""+stage_ID_list[int(stage_num)-1]+"\"}"}}
                            if i < 3:
                                fan_menu['footer']['contents'][0]['contents'].append(fan_element)
                            elif i>=3 and i<6 :
                                fan_menu['footer']['contents'][1]['contents'].append(fan_element)
                            elif i>=6 :
                                fan_menu['footer']['contents'][2]['contents'].append(fan_element)
                        contents.append(fan_menu)
                    if funtion_list[3] == '1':#負壓
                        print("負壓")
                        if NP_FAN_NUM <4:
                            np_fan_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif NP_FAN_NUM <7 and NP_FAN_NUM >=4:
                            np_fan_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            np_fan_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif NP_FAN_NUM >6 :
                            np_fan_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            np_fan_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            np_fan_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        for i in range(NP_FAN_NUM):
                            np_fan_element={"type": "button","action": {"type": "postback","label": str(i+1)+"號","data": "{\"SITE_NUM\":\""+stage_num+"\",\"SITE_NAME\":\""+control_ID+"\",\"Device\":\"負壓風扇\",\"control_Device\":\"NP_FAN\",\"status\":\""+status+"\",\"control_Status\":\""+control_Status+"\",\"NUM\":\""+str(i+1)+"\",\"control_ID\":\""+control_ID+"\",\"stage_name\":\""+stage_ID_list[int(stage_num)-1]+"\"}"}}
                            if i < 3:
                                np_fan_menu['footer']['contents'][0]['contents'].append(np_fan_element)
                            elif i>=3 and i<6 :
                                np_fan_menu['footer']['contents'][1]['contents'].append(np_fan_element)
                            elif i>=6 :
                                np_fan_menu['footer']['contents'][2]['contents'].append(np_fan_element)
                        contents.append(np_fan_menu)
                    if funtion_list[4] == '1':#噴霧
                        print("噴霧")
                        if WATER_NUM <4:
                            water_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif WATER_NUM <7 and WATER_NUM >=4:
                            water_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            water_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif WATER_NUM >6 :
                            water_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            water_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            water_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        for i in range(WATER_NUM):
                            water_element={"type": "button","action": {"type": "postback","label": str(i+1)+"號","data": "{\"SITE_NUM\":\""+stage_num+"\",\"SITE_NAME\":\""+control_ID+"\",\"Device\":\"噴霧迴路\",\"control_Device\":\"WATER\",\"status\":\""+status+"\",\"control_Status\":\""+control_Status+"\",\"NUM\":\""+str(i+1)+"\",\"control_ID\":\""+control_ID+"\",\"stage_name\":\""+stage_ID_list[int(stage_num)-1]+"\"}"}}
                            if i < 3:
                                water_menu['footer']['contents'][0]['contents'].append(water_element)
                            elif i>=3 and i<6 :
                                water_menu['footer']['contents'][1]['contents'].append(water_element)
                            elif i>=6 :
                                water_menu['footer']['contents'][2]['contents'].append(water_element)
                        contents.append(water_menu)

                    if funtion_list[5] == '1':#噴藥
                        print("噴藥")
                        if SPRAY_NUM <4:
                            spray_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif SPRAY_NUM <7 and SPRAY_NUM >=4:
                            spray_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            spray_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif SPRAY_NUM >6 :
                            spray_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            spray_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            spray_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        for i in range(SPRAY_NUM):
                            spray_element={"type": "button","action": {"type": "postback","label": str(i+1)+"號","data": "{\"SITE_NUM\":\""+stage_num+"\",\"SITE_NAME\":\""+control_ID+"\",\"Device\":\"噴藥迴路\",\"control_Device\":\"SPRAY\",\"status\":\""+status+"\",\"control_Status\":\""+control_Status+"\",\"NUM\":\""+str(i+1)+"\",\"control_ID\":\""+control_ID+"\",\"stage_name\":\""+stage_ID_list[int(stage_num)-1]+"\"}"}}
                            if i < 3:
                                spray_menu['footer']['contents'][0]['contents'].append(spray_element)
                            elif i>=3 and i<6 :
                                spray_menu['footer']['contents'][1]['contents'].append(spray_element)
                            elif i>=6 :
                                spray_menu['footer']['contents'][2]['contents'].append(spray_element)
                        contents.append(spray_menu)
                    
                    if funtion_list[7] == '1':#微噴
                        print("微噴")
                        if NUTRIEN_NUM <4:
                            nuirten_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif NUTRIEN_NUM <7 and NUTRIEN_NUM >=4:
                            nuirten_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            nuirten_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif NUTRIEN_NUM >6 :
                            nuirten_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            nuirten_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            nuirten_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        for i in range(NUTRIEN_NUM):
                            nuirten_element={"type": "button","action": {"type": "postback","label": str(i+1)+"號","data": "{\"SITE_NUM\":\""+stage_num+"\",\"SITE_NAME\":\""+control_ID+"\",\"Device\":\"微噴迴路\",\"control_Device\":\"NUTRIEN\",\"status\":\""+status+"\",\"control_Status\":\""+control_Status+"\",\"NUM\":\""+str(i+1)+"\",\"control_ID\":\""+control_ID+"\",\"stage_name\":\""+stage_ID_list[int(stage_num)-1]+"\"}"}}
                            if i < 3:
                                nuirten_menu['footer']['contents'][0]['contents'].append(nuirten_element)
                            elif i>=3 and i<6 :
                                nuirten_menu['footer']['contents'][1]['contents'].append(nuirten_element)
                            elif i>=6 :
                                nuirten_menu['footer']['contents'][2]['contents'].append(nuirten_element)
                                
                        contents.append(nuirten_menu)
                    
                    if funtion_list[6] == '1':#滴灌
                        print("滴灌")
                        if DI_NUM <4:
                            DI_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif DI_NUM <7 and DI_NUM >=4:
                            DI_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            DI_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif DI_NUM >6 :
                            DI_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            DI_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            DI_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        for i in range(DI_NUM):
                            DI_element={"type": "button","action": {"type": "postback","label": str(i+1)+"號","data": "{\"SITE_NUM\":\""+stage_num+"\",\"SITE_NAME\":\""+control_ID+"\",\"Device\":\"滴灌迴路\",\"control_Device\":\"D_I\",\"status\":\""+status+"\",\"control_Status\":\""+control_Status+"\",\"NUM\":\""+str(i+1)+"\",\"control_ID\":\""+control_ID+"\",\"stage_name\":\""+stage_ID_list[int(stage_num)-1]+"\"}"}}
                            if i < 3:
                                DI_menu['footer']['contents'][0]['contents'].append(DI_element)
                            elif i>=3 and i<6 :
                                DI_menu['footer']['contents'][1]['contents'].append(DI_element)
                            elif i>=6 :
                                DI_menu['footer']['contents'][2]['contents'].append(DI_element)
                        contents.append(DI_menu)
                    "////////"
                    if funtion_list[8] == '1':#遮陰
                        print("遮陰")
                        if SHADOW_NUM <4:
                            shadow_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif SHADOW_NUM <7 and SHADOW_NUM >=4:
                            shadow_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            shadow_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif SHADOW_NUM >6 :
                            shadow_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            shadow_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            shadow_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        for i in range(SHADOW_NUM):
                            shadow_element={"type": "button","action": {"type": "postback","label": str(i+1)+"號","data": "{\"SITE_NUM\":\""+stage_num+"\",\"SITE_NAME\":\""+control_ID+"\",\"Device\":\"遮陰迴路\",\"control_Device\":\"SHADOW\",\"status\":\""+status+"\",\"control_Status\":\""+control_Status+"\",\"NUM\":\""+str(i+1)+"\",\"control_ID\":\""+control_ID+"\",\"stage_name\":\""+stage_ID_list[int(stage_num)-1]+"\"}"}}
                            if i < 3:
                                shadow_menu['footer']['contents'][0]['contents'].append(shadow_element)
                            elif i>=3 and i<6 :
                                shadow_menu['footer']['contents'][1]['contents'].append(shadow_element)
                            elif i>=6 :
                                shadow_menu['footer']['contents'][2]['contents'].append(shadow_element)
                            
                        contents.append(shadow_menu)

                    if funtion_list[9] == '1':#捲揚
                        print("捲揚")
                        if WINCH_NUM <4:
                            winch_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif WINCH_NUM <7 and WINCH_NUM >=4:
                            winch_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            winch_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif WINCH_NUM >6 :
                            winch_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            winch_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            winch_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        for i in range(WINCH_NUM):
                            winch_element={"type": "button","action": {"type": "postback","label": str(i+1)+"號","data": "{\"SITE_NUM\":\""+stage_num+"\",\"SITE_NAME\":\""+control_ID+"\",\"Device\":\"捲揚迴路\",\"control_Device\":\"WINCH\",\"status\":\""+status+"\",\"control_Status\":\""+control_Status+"\",\"NUM\":\""+str(i+1)+"\",\"control_ID\":\""+control_ID+"\",\"stage_name\":\""+stage_ID_list[int(stage_num)-1]+"\"}"}}
                            if i < 3:
                                winch_menu['footer']['contents'][0]['contents'].append(winch_element)
                            elif i>=3 and i<6 :
                                winch_menu['footer']['contents'][1]['contents'].append(winch_element)
                            elif i>=6 :
                                winch_menu['footer']['contents'][2]['contents'].append(winch_element)
                        contents.append(winch_menu)

                    if funtion_list[10] == '1':#天窗
                        print("天窗")
                        if SKY_NUM <4:
                            sky_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif SKY_NUM <7 and SKY_NUM >=4:
                            sky_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            sky_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif SKY_NUM >6 :
                            sky_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            sky_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            sky_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        for i in range(SKY_NUM):
                            sky_element={"type": "button","action": {"type": "postback","label": str(i+1)+"號","data": "{\"SITE_NUM\":\""+stage_num+"\",\"SITE_NAME\":\""+control_ID+"\",\"Device\":\"天窗迴路\",\"control_Device\":\"SKY\",\"status\":\""+status+"\",\"control_Status\":\""+control_Status+"\",\"NUM\":\""+str(i+1)+"\",\"control_ID\":\""+control_ID+"\",\"stage_name\":\""+stage_ID_list[int(stage_num)-1]+"\"}"}}
                            if i < 3:
                                sky_menu['footer']['contents'][0]['contents'].append(sky_element)
                            elif i>=3 and i<6 :
                                sky_menu['footer']['contents'][1]['contents'].append(sky_element)
                            elif i>=6 :
                                sky_menu['footer']['contents'][2]['contents'].append(sky_element)
                        contents.append(sky_menu)

                    if funtion_list[11] == '1':#植物燈
                        print("植物燈")
                        if LAMP_NUM <4:
                            lamp_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif LAMP_NUM <7 and LAMP_NUM >=4:
                            lamp_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            lamp_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif LAMP_NUM >6 :
                            lamp_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            lamp_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            lamp_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        for i in range(LAMP_NUM):
                            lamp_element={"type": "button","action": {"type": "postback","label": str(i+1)+"號","data": "{\"SITE_NUM\":\""+stage_num+"\",\"SITE_NAME\":\""+control_ID+"\",\"Device\":\"植物燈迴路\",\"control_Device\":\"LAMP\",\"status\":\""+status+"\",\"control_Status\":\""+control_Status+"\",\"NUM\":\""+str(i+1)+"\",\"control_ID\":\""+control_ID+"\",\"stage_name\":\""+stage_ID_list[int(stage_num)-1]+"\"}"}}
                            if i < 3:
                                lamp_menu['footer']['contents'][0]['contents'].append(lamp_element)
                            elif i>=3 and i<6 :
                                lamp_menu['footer']['contents'][1]['contents'].append(lamp_element)
                            elif i>=6 :
                                lamp_menu['footer']['contents'][2]['contents'].append(lamp_element)
                        contents.append(lamp_menu)
                    content = {"type": "carousel"}
                    content.update({"contents": contents}) #將選單容器放進更大的容器中
                    message=FlexSendMessage(alt_text='控制選單',contents=content) #LINE_BOT包裝
                    line_bot_api.reply_message( event.reply_token, message) #將LINE_BOT包裝 推送給使用者
                    control_ID=None
                    stage_num=None
                elif status=="停止" :
                    if funtion_list[8] == '1':#遮陰
                        if SHADOW_NUM <4:
                            shadow_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif SHADOW_NUM <7 and SHADOW_NUM >=4:
                            shadow_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            shadow_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif SHADOW_NUM >6 :
                            shadow_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            shadow_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            shadow_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        for i in range(SHADOW_NUM):
                            shadow_element={"type": "button","action": {"type": "postback","label": str(i+1)+"號","data": "{\"SITE_NUM\":\""+stage_num+"\",\"SITE_NAME\":\""+control_ID+"\",\"Device\":\"遮陰迴路\",\"control_Device\":\"SHADOW\",\"status\":\""+status+"\",\"control_Status\":\""+control_Status+"\",\"NUM\":\""+str(i+1)+"\",\"control_ID\":\""+control_ID+"\",\"stage_name\":\""+stage_ID_list[int(stage_num)-1]+"\"}"}}
                            if i < 3:
                                shadow_menu['footer']['contents'][0]['contents'].append(shadow_element)
                            elif i>=3 and i<6 :
                                shadow_menu['footer']['contents'][1]['contents'].append(shadow_element)
                            elif i>=6 :
                                shadow_menu['footer']['contents'][2]['contents'].append(shadow_element)
                            
                        contents.append(shadow_menu)

                    if funtion_list[9] == '1':#捲揚
                        if WINCH_NUM <4:
                            winch_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif WINCH_NUM <7 and WINCH_NUM >=4:
                            winch_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            winch_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif WINCH_NUM >6 :
                            winch_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            winch_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            winch_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        for i in range(WINCH_NUM):
                            winch_element={"type": "button","action": {"type": "postback","label": str(i+1)+"號","data": "{\"SITE_NUM\":\""+stage_num+"\",\"SITE_NAME\":\""+control_ID+"\",\"Device\":\"捲揚迴路\",\"control_Device\":\"WINCH\",\"status\":\""+status+"\",\"control_Status\":\""+control_Status+"\",\"NUM\":\""+str(i+1)+"\",\"control_ID\":\""+control_ID+"\",\"stage_name\":\""+stage_ID_list[int(stage_num)-1]+"\"}"}}
                            if i < 3:
                                winch_menu['footer']['contents'][0]['contents'].append(winch_element)
                            elif i>=3 and i<6 :
                                winch_menu['footer']['contents'][1]['contents'].append(winch_element)
                            elif i>=6 :
                                winch_menu['footer']['contents'][2]['contents'].append(winch_element)
                        contents.append(winch_menu)

                    if funtion_list[10] == '1':#天窗
                        if SKY_NUM <4:
                            sky_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif SKY_NUM <7 and SKY_NUM >=4:
                            sky_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            sky_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        elif SKY_NUM >6 :
                            sky_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            sky_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                            sky_menu['footer']['contents'].append({"type": "box","layout": "horizontal","contents": []})
                        for i in range(SKY_NUM):
                            sky_element={"type": "button","action": {"type": "postback","label": str(i+1)+"號","data": "{\"SITE_NUM\":\""+stage_num+"\",\"SITE_NAME\":\""+control_ID+"\",\"Device\":\"天窗迴路\",\"control_Device\":\"SKY\",\"status\":\""+status+"\",\"control_Status\":\""+control_Status+"\",\"NUM\":\""+str(i+1)+"\",\"control_ID\":\""+control_ID+"\",\"stage_name\":\""+stage_ID_list[int(stage_num)-1]+"\"}"}}
                            if i < 3:
                                sky_menu['footer']['contents'][0]['contents'].append(sky_element)
                            elif i>=3 and i<6 :
                                sky_menu['footer']['contents'][1]['contents'].append(sky_element)
                            elif i>=6 :
                                sky_menu['footer']['contents'][2]['contents'].append(sky_element)
                        contents.append(sky_menu)
                    #更大的選單容器
                    content = {"type": "carousel"}
                    content.update({"contents": contents}) #將選單容器放進更大的容器中
                    message=FlexSendMessage(alt_text='控制選單',contents=content) #LINE_BOT包裝
                    line_bot_api.reply_message( event.reply_token, message) #將LINE_BOT包裝 推送給使用者
                    control_ID=None
                    stage_num=None

        else :
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="請重新進入控制選單 選擇場域與狀態")
                )


                



#使用者選擇設備編號開關後 進行後台運作
@handler.add(PostbackEvent)
def handle_postback(event):
#這裡放你要做的事情

    ts = event.postback.data
    if ts!= "richmenu-changed-to-a" and ts!= "richmenu-changed-to-b":
        DATA=json.loads(ts)
        print (DATA)
        NEW_url="http://yuanmqtt.ddns.net:3650/Control_Device?Device="+DATA['control_Device']+"&NUM="+DATA['NUM']+"&Status="+DATA['control_Status']+"&userID="+DATA['SITE_NAME']+"&SITE="+DATA['SITE_NUM']
        #print (url)
        response = requests.get(url=NEW_url)
        #print(response.status_code)
        #print(response.text)
        if response.status_code==200:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=DATA['SITE_NAME']+"\n場域 : "+DATA['stage_name']+"\n"+DATA['Device']+DATA['NUM']+"號 狀態:"+DATA['status'])
                )



if __name__ == "__main__":
    app.run()

