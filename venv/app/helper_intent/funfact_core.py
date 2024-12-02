from linebot.models import *
from linebot import *
from app import app, db
from app.models.leave import Leave
from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)
from datetime import datetime, timedelta
import json
import requests

LINE_BOT_API=app.config['LINE_BOT_API']
HANDLER=app.config['HANDLER']
line_bot_api = LineBotApi(LINE_BOT_API)
handler = WebhookHandler(HANDLER)

def funfact_core(intent,text,reply_token):
    if intent == 'fun-and-fact-cat_f':
        url_img = "https://api.thecatapi.com/v1/images/search"
        url_fact = "https://catfact.ninja/fact"
        response_img = requests.get(url_img)
        response_fact = requests.get(url_fact)
        data_img = response_img.json()
        data_fact = response_fact.json()
        cat_img = data_img[0]['url']
        cat_fact = data_fact['fact']
       
        image_message = ImageSendMessage(original_content_url=cat_img, preview_image_url=cat_img)
        # line_bot_api.reply_message(reply_token, image_message)
        
        text_message = TextSendMessage(text=cat_fact)
        line_bot_api.reply_message(reply_token, [image_message, text_message])
    
    if intent == 'fun-and-fact-nasa_f':
        API_KEY  = app.config['NASA_API_KEY']
        url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"
        response = requests.get(url)
        data = response.json()
        title = data['title']
        date = data['date']
        content = data['explanation']
        img = data['url']
        
        text_message = TextSendMessage(text="Data from NASA\nTitle : {}\nData : {}\nExplanation :\n{}".format(title,date,content))
        image_message = ImageSendMessage(original_content_url=img, preview_image_url=img)
        line_bot_api.reply_message(reply_token, [image_message, text_message])
    
    if intent == 'fun-and-fact-joke_f':
        url = "https://v2.jokeapi.dev/joke/Programming?type=single"
        response = requests.get(url)
        data = response.json()
        joke = data['joke']
        text_message = TextSendMessage(text=joke)
        line_bot_api.reply_message(reply_token,text_message)