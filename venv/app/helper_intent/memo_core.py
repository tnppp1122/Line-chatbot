from linebot.models import *
from linebot import *
from app import app, db
from app.models.memo import Memo
from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)
from datetime import datetime, timedelta
import json

LINE_BOT_API=app.config['LINE_BOT_API']
HANDLER=app.config['HANDLER']
line_bot_api = LineBotApi(LINE_BOT_API)
handler = WebhookHandler(HANDLER)

def memo_core(intent,text,reply_token):
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
    
    if intent == "Last_Day":
    
        filtered_memos = []
        for memo in Memo.query.all():  
            if memo.deadline is not None:
        
                date = memo.date.strftime("%d-%m-%Y")
                
                date1=datetime.strptime(date, "%d-%m-%Y")
                print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                print(memo.deadline)
                deadline=datetime.strptime(memo.deadline, "%d-%m-%Y")
           
                time_diff = date1 - deadline
              
                if abs(time_diff) <= timedelta(hours=24):
                    filtered_memos.append(memo)
            
        message_text = "รายการทั้งหมด \n"
        for memo in filtered_memos:
            message_text += "หัวข้อ : {}\nเนื้อหา : {}\nวันที่ : {}\nกำหนดส่ง : {}\n\n".format(
                memo.topic, memo.content, memo.date, memo.deadline
            )

        text_message = TextSendMessage(text=message_text)
        line_bot_api.reply_message(reply_token, text_message)