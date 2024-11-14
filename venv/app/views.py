import json
from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)


from sqlalchemy.sql import text
from app import app
from app import db
from app import os
from app import basedir
import random
import secrets
import string
from linebot.models import *
from linebot import *
from app.models.test import Test
from urllib.request import urlopen
import json
from urllib.parse import quote
import ast
from app.models.memo import Memo
from datetime import datetime, timedelta

@app.route('/')
def home():
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    new=Test(
        firstname="I'm the king of the world!!!"
    )
    db.session.add(new)
    db.session.commit()
    return "hello, world"

@app.route('/t')
def t():
    t = Memo.query.all()
    t_l = []
    for i in t:
        x={
            'topic' : i.topic,
            'content' : i.content,
            'date' : i.date,
            'deadline' : i.deadline
            
        }
        t_l.append(x)
    return jsonify(t_l)


LINE_BOT_API=app.config['LINE_BOT_API']
HANDLER=app.config['HANDLER']
line_bot_api = LineBotApi(LINE_BOT_API)
handler = WebhookHandler(HANDLER)


@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    # print(body)
    req = request.get_json(silent=True, force=True)
    intent = req["queryResult"]["intent"]["displayName"] 
    text = req['originalDetectIntentRequest']['payload']['data']['message']['text'] 
    reply_token = req['originalDetectIntentRequest']['payload']['data']['replyToken']
    id = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    # disname = line_bot_api.get_profile(id).display_name

    first_line = text.splitlines()[0]
    print('id = ' + id)
    # print('name = ' + disname)
    print('text = ' + text)
    print('first_line_text = ' + first_line)
    print('intent = ' + intent)
    print('reply_token = ' + reply_token)
    reply(intent,text,reply_token,id)

    return 'OK'


def reply(intent,text,reply_token,id):
    if intent == 'test_f':
        text_message = TextSendMessage(text='ทดสอบสำเร็จ')
        line_bot_api.reply_message(reply_token,text_message)
        
    if intent == 'rose_f':
        m_link=app.config['IMAGE_LINK']
        image_links = ast.literal_eval(m_link)
        chosen_image = random.choice(image_links)        
        image_message = ImageSendMessage(
            original_content_url=chosen_image['original'],
            preview_image_url=chosen_image['preview']
        )
        line_bot_api.reply_message(reply_token, image_message)
        
    if intent == 'weather_f - custom':
        spilt_text = text.splitlines()
        city = spilt_text[1]
        decode = quote(city)
        token = app.config['WEATHER_TOKEN']
        api_url = 'https://api.waqi.info/feed/'+decode+'/?token='+token
        res = urlopen(api_url)
        w_data = json.loads(res.read())
        json_weather = {
                'AQI': w_data['data']['aqi'],
                'PM2.5': w_data['data']['iaqi']['pm25']['v'],
                'Temperature': w_data['data']['iaqi']['t']['v'],
                'Time': w_data['data']['time']['s'] 
            }
        aqi = json_weather['AQI']
        pm25 = str(json_weather['PM2.5']) 
        Temperature = str(json_weather['Temperature'])
        Time = str(json_weather['Time'])
        text_message = TextSendMessage(
            text='สภาพอากาศ : {}\nAQI = {}\nPM25 = {}\nอุณหภูมิ = {}\nเวลา = {}'.format(
                city, aqi, pm25, Temperature, Time))
        line_bot_api.reply_message(reply_token,text_message)
    
    if intent == 'Explain - custom':
        spilt_text = text.splitlines()
        print(spilt_text)
        topic = spilt_text[1]
        content = spilt_text[2]
        memo_index=Memo(
            topic=topic,
            content=content
        )
        db.session.add(memo_index)
        db.session.commit()
        
        text_message = TextSendMessage(
            text='Topic : {}\nบันทึกสำเร็จ'.format(topic))
        line_bot_api.reply_message(reply_token,text_message)
        
    if intent == 'Remind - custom':
        spilt_text = text.splitlines()
        print(spilt_text)
        topic = spilt_text[1]
        content = spilt_text[2]
        deadline = spilt_text[3]
        # print(spilt_text)
        memo_index=Memo(
            topic=topic,
            content=content,
            deadline=deadline
        )
        db.session.add(memo_index)
        db.session.commit()
        
        text_message = TextSendMessage(
            text='เตือน : {}\nบันทึกสำเร็จ'.format(topic))
        line_bot_api.reply_message(reply_token,text_message)
    
    if intent == "LIST":
        memo_db = Memo.query.all()
        list_topic = []
        for i in memo_db:
            topic={
                'topic' : i.topic,
                'content' : i.content,
                'date' : i.date,
                'deadline' : i.deadline
            }
            list_topic.append(topic)
        json_topic = jsonify(list_topic)
        
        message_text = "รายการทั้งหมด \n"
        for topic in list_topic:
            message_text += "หัวข้อ : {}\nเนื้อหา : {}\nวันที่ : {}\nกำหนดส่ง : {}\n\n".format(
                topic['topic'], topic['content'], topic['date'], topic['deadline']
            )

        text_message = TextSendMessage(text=message_text)
        line_bot_api.reply_message(reply_token, text_message)
    
    if intent == "Open_file - custom":
        spilt_text = text.splitlines()
        print(spilt_text)
        topic = spilt_text[1]
        memo_db_filter = Memo.query.filter(Memo.topic==topic).all()
        list_topic = []
        for i in memo_db_filter:
            topic={
                'topic' : i.topic,
                'content' : i.content,
                'date' : i.date,
                'deadline' : i.deadline
            }
            list_topic.append(topic)
        json_topic = jsonify(list_topic)

        text_message = TextSendMessage(
            text="หัวข้อ : {}\nเนื้อหา : {}\nวันที่ : {}\nกำหนดส่ง : {}\n\n".format(
                topic['topic'], topic['content'], topic['date'], topic['deadline'])
            )
        line_bot_api.reply_message(reply_token,text_message)
        
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
