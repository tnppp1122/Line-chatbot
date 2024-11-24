from linebot.models import *
from linebot import *
from app import app, db
from app.models.leave import Leave
from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)
from datetime import datetime, timedelta
import json

LINE_BOT_API=app.config['LINE_BOT_API']
HANDLER=app.config['HANDLER']
line_bot_api = LineBotApi(LINE_BOT_API)
handler = WebhookHandler(HANDLER)

def leave_core(intent,text,reply_token):
    if intent == 'add-program - custom':
        spilt_text = text.splitlines()
        program = spilt_text[1]
        leave_total = spilt_text[2]
        leave_index=Leave(
            program=program,
            total_leave=leave_total
        )
        db.session.add(leave_index)
        db.session.commit()
        text_message = TextSendMessage(
            text='บันทึก : {} สำเร็จ'.format(program))
        line_bot_api.reply_message(reply_token,text_message)
        
    if intent == "add-leave-day - custom":
        spilt_text = text.splitlines()
        program = spilt_text[1]
        leave = spilt_text[2]
        leave_db_filter = Leave.query.filter(Leave.program==program).all()
        if leave_db_filter:
            for item in leave_db_filter:
                if item.leave == None:
                    item.leave = int(leave)
                else:
                    item.leave += int(leave)  
        else:
            new_leave = Leave(program=program, leave=leave)
            db.session.add(new_leave)
        db.session.commit()
        text_message = TextSendMessage(
            text='ลงบันทึกวันลา : {} สำเร็จ'.format(program))
        line_bot_api.reply_message(reply_token,text_message)

    if intent == 'list-leave':
        leave_db = Leave.query.all()
        list_leave = []
        for i in leave_db:
            leave_index={
                'program' : i.program,
                'total' : i.total_leave,
                'leave' : i.leave,
            }
            list_leave.append(leave_index)
        # json_leave = jsonify(list_leave)
        message_text = "รายการทั้งหมด \n"
        for l in list_leave:
            message_text += "program : {}\nจำนวนวันลาทั้งหมด : {}\nจำนวนวันที่เคยลา : {}\n".format(
                l['program'], l['total'], l['leave']
            )
        text_message = TextSendMessage(text=message_text)
        line_bot_api.reply_message(reply_token, text_message)