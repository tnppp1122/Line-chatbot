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

@app.route('/')
def home():

    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    new=Test(
        firstname="somsom"
    )
    db.session.add(new)
    db.session.commit()
    return "hello world"

@app.route('/t')
def t():
    t = Test.query.all()
    t_l = []
    for i in t:
        x={
            'firstname' : i.firstname
        }
        t_l.append(x)
    return jsonify(t_l)

@app.route('/db')
def db_connection():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return '<h1>db works.</h1>'
    except Exception as e:
        return '<h1>db is broken.</h1>' + str(e)

@app.route('/crash')
def crash():
    return 1/0


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
    disname = line_bot_api.get_profile(id).display_name

    print('id = ' + id)
    print('name = ' + disname)
    print('text = ' + text)
    print('intent = ' + intent)
    print('reply_token = ' + reply_token)
    
    reply(intent,text,reply_token,id,disname)

    return 'OK'


def reply(intent,text,reply_token,id,disname):
    if intent == 'ทดสอบ':
        text_message = TextSendMessage(text='ทดสอบสำเร็จ')
        line_bot_api.reply_message(reply_token,text_message)
        
    
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
