# -*- coding: utf-8 -*-
"""
Created on Sat May  8 15:33:10 2021

@author: Admin
"""

import telebot
import dbConnect as db

#from telebot import types
PROXY='http//69.167.174.17:80'
# telebot.apihelper.proxy = {'http': PROXY}
bot = telebot.TeleBot("1472330029:AAHJ7ZcbEmRWzJ7PrVwg4Ln1jdk6LxIJDXo")
#bot = telebot.TeleBot("1735621887:AAGxSJe60yBfv_2Jd8xhUyc-BTlMeKhdIMI")
id_m='1486120266'
def send_notify(msg,id_u,rf):
    users=db.executeSql('select * from search where UID={} and ref="{}"'.format(id_u,rf))[0][2].split('@')
    if len(users)>1:
        for user in users:
            bot.send_message(user,msg)

    bot.send_message(id_u, msg)
        
    
    
    
        
    
    


        
        
                
def send_call(msg,id_u):
   
    users=db.executeSql('select  * from users')
    for user in users:
        if id_u!=user[0]:
            bot.send_message(user[0],msg)

