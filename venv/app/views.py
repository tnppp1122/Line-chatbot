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
        
    if intent == 'rose':
        image_links = [
            {'original': 'https://i.pinimg.com/564x/06/fd/71/06fd71d931657acfd6dc128c914842d4.jpg', 'preview': 'https://i.pinimg.com/564x/06/fd/71/06fd71d931657acfd6dc128c914842d4.jpg'},
            {'original': 'https://i.pinimg.com/564x/c0/c7/7c/c0c77c79f82a14dc9107b6602d6aef1f.jpg', 'preview': 'https://i.pinimg.com/564x/c0/c7/7c/c0c77c79f82a14dc9107b6602d6aef1f.jpg'},
            {'original': 'https://i.pinimg.com/564x/95/0f/4f/950f4f90ff334ad7e645084edc9f89be.jpg', 'preview': 'https://i.pinimg.com/564x/95/0f/4f/950f4f90ff334ad7e645084edc9f89be.jpg'},
            {'original': 'https://i.pinimg.com/564x/d2/b7/ad/d2b7adc3478744852d83e681b0f50040.jpg', 'preview': 'https://i.pinimg.com/564x/d2/b7/ad/d2b7adc3478744852d83e681b0f50040.jpg'},
            {'original': 'https://i.pinimg.com/736x/56/ca/e3/56cae392dbbf1f1e27789a457193d4cd.jpg', 'preview': 'https://i.pinimg.com/736x/56/ca/e3/56cae392dbbf1f1e27789a457193d4cd.jpg'},
            {'original': 'https://i.pinimg.com/564x/34/81/a7/3481a7bd322085a3815651e03ec3a721.jpg', 'preview': 'https://i.pinimg.com/564x/34/81/a7/3481a7bd322085a3815651e03ec3a721.jpg'},
            {'original': 'https://i.pinimg.com/564x/4f/34/d2/4f34d2dad8546b06aeb42f8e067ef733.jpg', 'preview': 'https://i.pinimg.com/564x/4f/34/d2/4f34d2dad8546b06aeb42f8e067ef733.jpg'},
            {'original': 'https://i.pinimg.com/564x/2e/88/ca/2e88ca4472d3c97ff5802f9dbb20a8c8.jpg', 'preview': 'https://i.pinimg.com/564x/2e/88/ca/2e88ca4472d3c97ff5802f9dbb20a8c8.jpg'},
            {'original': 'https://i.pinimg.com/564x/a4/15/04/a4150473d1bed9954a5ffdf196d19e8a.jpg', 'preview': 'https://i.pinimg.com/564x/a4/15/04/a4150473d1bed9954a5ffdf196d19e8a.jpg'}
        ]

        chosen_image = random.choice(image_links)        
        image_message = ImageSendMessage(
            original_content_url=chosen_image['original'],
            preview_image_url=chosen_image['preview']
        )
        line_bot_api.reply_message(reply_token, image_message)
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
