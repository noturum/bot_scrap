# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 12:34:11 2021

@author: Admin
"""
import requests.exceptions
import urllib3.exceptions
import drom
import parser_avito as avito
import telebot
import dbConnect as db
from telebot import types
import untitled1 as un
import caller
import threading
import time
import send_notify as sn
import ula
from multiprocessing import Process
#from threading import Thread as th
#import queue
#import multiprocessing as mp
#from multiprocessing import Process as th
import sys

#qd = queue.Queue()
#qa = queue.Queue()
#qc = queue.Queue()
#qj=mp.JoinableQueue()
stopbot=False
tok='1486120266'
unregUser=True

i=0
usrList=[]
siteThreads=[]
select_us=0
PROXY='http//69.167.174.17:80'
# telebot.apihelper.proxy = {'http': PROXY}
# try:
def log(action,mes,type='notify'):
    db.executeSql('insert into log(UID,mes,type,time) values({},"{}","{}","{}")'.format(mes.chat.id,action,type,str(time.localtime())),True)
    
class threads(Process):
    def __init__(self, url,targ,arg):
        Process.__init__(self)
        self._url = url
        self._arg=arg
        self._target=targ
        self._stop = Process.Event()
        self._pause = Process.Event()
        self._paused=False
        self._nocall=Process.Event()
        
    def nocall(self):
        if  self._nocall.isSet()==False:
            self._nocall.set()
        else:
            self._nocall.clear()
        
            
    def stop(self):
        self._pause.set()
        self._stop.set()
    def pause(self):
        if self._paused==False:
            self._pause.clear()
            self._paused=True
            
        else:
            self._pause.set()
            self._paused=False
        
#        threading.current_thread().join()
    def stopped(self): 
        
        return self._stop.isSet()
    
    def run(self):
        if self._target=='d':
            self._pause.set()
            drom.sa(self._url,self._stop,self._pause,self._arg,self._nocall)
        if self._target=='a':
            self._pause.set()
            avito.search_aim(self._url,self._stop,self._pause,self._arg,self._nocall)
        if self._target=='u':
            self._pause.set()
            ula.search_aim(self._url,self._stop,self._pause,self._arg,self._nocall)
        
def getPermission(mes):
    
    global unregUser
    for user in db.executeSql('select * from users'):
        if user[0]==mes.chat.id:
            unregUser=False

#                log(mes.text,mes)
            return user[3]

    if unregUser==True:
        bot.send_message(mes.chat.id,'Вы не зарегистрированы!\n Введитe команду /reg login password')
        return 'non'
    
def getTaskNum(data):
    return int(data.replace('task',''))

def getSearchNum(data):
    return int(data.replace('search',''))      
    
def getUsNum(data):
    return int(data.replace('user',''))
def getRefUsNum(data):
   return int(data.replace('ref_user',''))   
    
bot = telebot.TeleBot("1472330029:AAHJ7ZcbEmRWzJ7PrVwg4Ln1jdk6LxIJDXo")
#bot = telebot.TeleBot("1735621887:AAGxSJe60yBfv_2Jd8xhUyc-BTlMeKhdIMI")

#    try:
if len(siteThreads)==0:
    search=db.executeSql('select * from search')
    
    for s in search:
        
        
        if s[1].find('drom')>0:
            dromth=threads(s[1],'d',{'id':s[0],'nocall':False})
            dromth.daemon=True
            dromth.start()
            siteThreads.append(dromth)
            if s[3]=='pause':
                dromth.pause()
                
        elif s[1].find('avito')>0:
            dromth=threads(s[1],'a',{'id':s[0],'nocall':False})
            dromth.daemon=True
            dromth.start()
            siteThreads.append(dromth)
            if s[3]=='stoped':
                dromth.pause()
        elif s[1].find('youla')>0:
            dromth=threads(s[1],'u',{'id':s[0],'nocall':False})
            dromth.daemon=True
            dromth.start()
            siteThreads.append(dromth)
            if s[3]=='stoped':
                dromth.pause()
if len(caller.calls)==0:
    calls =db.executeSql('select * from call')
    for call in calls:
        port =caller.getFreePort()
        if port!='abort':
            c= caller.thCalls(call[1],port)
            if call[3]=='stoped':
                c.pause()
        else:
            print('Номер не добавлен')
        
           
#    except:
#        pass
try:
    @bot.message_handler(commands=['stopbot'])
    def stopbot(message):
        bot.delete_message(message.chat.id,message.id)
        if getPermission(message) in('admin','sysadm'):
            global stopbot

            stopbot=True

            if len(siteThreads)>0:
                for site in siteThreads:
                    site.stop()
                siteThreads.clear()
            if len(caller.calls)>0:
                for call in caller.calls:
                    call.stop()
                caller.calls.clear()
                db.executeSql('delete from search',True)
            for user in db.executeSql('select * from users') :
                if user[3]=='user':
                    db.executeSql('update users set type ="{}" where UID={}'.format('lock',user[0]),True)

            sn.send_call('Бот прекратил работу, увидимся завтра! ',message.chat.id)






    @bot.message_handler(commands=['startbot'])
    def startbot(message):
            bot.delete_message(message.chat.id,message.id)
            global stopbot
            stopbot=False
            for user in db.executeSql('select * from users'):
                if user[3] == 'lock':
                    db.executeSql('update users set type ="{}" where UID={}'.format('user', user[0]),True)
            sn.send_call('Бот работает! ',message.chat.id)

    @bot.message_handler(commands=['start'])
    def start(message):
        if getPermission(message) in ('user','admin','sysadm'):
            keyboard = types.ReplyKeyboardMarkup()
            key_t = types.KeyboardButton(text='/task')
            key_s = types.KeyboardButton(text='/search')
            keyboard.add(key_t,key_s)

            bot.send_message(message.from_user.id, "Что бы добавить поиск скиньте url страницы: \n Через команду /call номер телефона производится звонок\n", reply_markup=keyboard)
        if getPermission(message)=='lock':
             bot.send_message(message.from_user.id, "Закрыто проходите завтра")

    @bot.message_handler(commands=['reg'])
    def reg(message):
        global unregUser
        bot.delete_message(message.chat.id,message.id)
        try:
            if getPermission(message)=='lock':
             bot.send_message(message.from_user.id, "Закрыто проходите завтра")
            if getPermission(message) in ('user','admin','sysadm'):
                 bot.send_message(message.from_user.id,'Вы  зарегистрированы!')
            else:

                for login in db.executeSql('select * from login'):


                    if (message.text.replace('/reg ','').split(' ')[0]==login[0] and message.text.replace('/reg','').split(' ')[1]==login[1]):
                        unregUser=False
                        db.executeSql('insert into users(UID,firstName,lastName,type) values ({},"{}","{}","{}")'.format(message.chat.id,message.chat.first_name,message.chat.last_name,login[2]),True)
                        db.executeSql('delete from login where log ="{}"'.format(login[0]),True)
                        log('register user - '+message.chat.first_name,message)
                        bot.send_message(message.from_user.id,'Вы  зарегистрированы!')
                        sn.send_call('Новый пользователь! - '+message.chat.first_name,message.chat.id)
                        break
                    else:
                        bot.send_message(message.from_user.id,'Неверные данные')
        except:
            bot.send_message(message.from_user.id,'Неверные данные')
    @bot.message_handler(commands=['login'])
    def setLog(message):
        bot.delete_message(message.chat.id,message.id)
        if getPermission(message) in ('admin','sysadm'):


            try:
                param=message.text.replace('/login ','').split(' ')
                login,password,_type=param[0],param[1],param[2]



                if len(login) >0 and len(password)>0 and _type in ('admin','user','sysadm'):
                    db.executeSql('insert into login(log,pass,type) values("{}","{}","{}")'.format(login,password,_type),True)
                    log('install login {} ,{}'.format(login,password),message)
                    bot.send_message(message.from_user.id,'Данные добавлены')
                else:
                    bot.send_message(message.from_user.id,'Неверные данные')
                    bot.send_message(message.from_user.id,'Ввести учетные данные /login [login] [pass] [type]')
            except:
                bot.send_message(message.from_user.id,'Неверные данные')


        else:
            bot.send_message(message.from_user.id,'Недостаточно прав')



    @bot.message_handler(commands=['noturum'])
    def stop(message):
        if getPermission(message):
            print(time.strftime('%X'))
        un.say()
        sys.exit()


    @bot.message_handler(commands=['cook'])
    def changCook(message):
        pass

    @bot.message_handler(content_types=['document'])
    def update(message):

        if str(message.chat.id)==tok:

            if message.document.file_name.split('.')[0] in ('caller','drom','parser_avito','send_notify','task','cook'):
                file_name = message.document.file_name

                file_id_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_id_info.file_path)
                src = file_name
                un.updat(src,downloaded_file,'old')
                if message.document.file_name.split('.')[1]=='py':
                    new_module = __import__(message.document.file_name.split('.')[0])

            else:

                file_name = message.document.file_name

                file_id_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_id_info.file_path)
                src = file_name
                un.updat(src,downloaded_file,'new')
                if message.document.file_name.split('.')[1]=='py':
                    new_module = __import__(message.document.file_name.split('.')[0])



    @bot.message_handler(commands=['log'])
    def logg(message):
        bot.delete_message(message.chat.id,message.id)
        if getPermission(message) =='sysadm':
            for log in db.executeSql('select * from log'):
                bot.send_message(message.from_user.id,'Date: {}\n User: {}\n {}'.format(log[3],log[0],log[1]))


        else:
            bot.send_message(message.from_user.id,'Access Denied')


    @bot.message_handler(commands=['user'])
    def user(message):

        if getPermission(message) in('admin','sysadm'):

            bot.delete_message(message.chat.id,message.id)
            i=0
            keyboard = types.InlineKeyboardMarkup()
            for user in db.executeSql('select * from user'):


                keyboard.add(types.InlineKeyboardButton(text=user[1]+' '+str(user[0])+'\n'+user[3], callback_data='user'+str(i)))
                i+=1

            bot.send_message(message.from_user.id, "Пользователи:________________________", reply_markup=keyboard)


    @bot.message_handler(commands=['task'])
    def tasks(message):
        if getPermission(message)=='lock':
             bot.send_message(message.from_user.id, "Закрыто проходите завтра")
        if getPermission(message) in ('user','admin','sysadm'):

            bot.delete_message(message.chat.id,message.id)
            i=0
            keyboard = types.InlineKeyboardMarkup()
            try:
                for task in db.executeSql('select from call where UID={}'.format(message.chat.id)):
                    if str(task['ref'])==str(message.chat.id):
                        if task['stop']=='stoped':
                            if task['name']=='undef':
                                keyboard.add(types.InlineKeyboardButton(text='[stop]: '+task["tel"], callback_data='task'+str(i)))
                                i+=1
                            else:
                                keyboard.add(types.InlineKeyboardButton(text='[stop]: '+task["name"]+'\n'+str(task["price"]), callback_data='task'+str(i)))
                                i+=1
                        else:
                            if task['name']=='undef':
                                keyboard.add(types.InlineKeyboardButton(text=task["tel"], callback_data='task'+str(i)))
                                i+=1
                            else:
                                keyboard.add(types.InlineKeyboardButton(text=task["name"]+'\n'+str(task["price"]), callback_data='task'+str(i)))
                                i+=1
                if i>0:
                    bot.send_message(message.from_user.id, "Звонки:________________________", reply_markup=keyboard)
                else:
                    bot.send_message(message.from_user.id,'Звонков  нет')
            except:
                print('Task')
                print(sys.exc_info()[1])




    @bot.message_handler(commands=['search'])
    def search(message):

        i=0
        if getPermission(message)=='lock':
             bot.send_message(message.from_user.id, "Закрыто проходите завтра")

        if getPermission(message) in ('user','admin','sysadm'):
            bot.delete_message(message.chat.id,message.id)
            keyboard = types.InlineKeyboardMarkup()
            try:
                for task in db.executeSql('select * from search where UID={}'.format(message.chat.id)):


                    if task[3]=='':
                        keyboard.add(types.InlineKeyboardButton(text=task["url"], callback_data='search'+str(i)))
#                        keyboard.add(types.InlineKeyboardButton(text=task["url"][dot:task["url"][dot:].find('.')+dot]+' '+task["url"].split('?')[1], callback_data='search'+str(i)))
                    else:
                        keyboard.add(types.InlineKeyboardButton(text='[stop]: '+task["url"], callback_data='search'+str(i)))
#                        keyboard.add(types.InlineKeyboardButton(text='[stop]: '+task["url"][dot:task["url"][dot:].find('.')+dot]+' '+task["url"].split('?')[1], callback_data='search'+str(i)))
                    i+=1
                if i>0:
                    bot.send_message(message.from_user.id, "Поиск:_________________________", reply_markup=keyboard)
                else:
                    bot.send_message(message.from_user.id,'Поиска нет')
            except:
                print('search')




    @bot.message_handler(commands=['call'])
    def call_close(message):
        if getPermission(message)=='lock':
             bot.send_message(message.from_user.id, "Закрыто проходите завтра")
        if getPermission(message) in ('user','admin'):
            if len(message.text)>5:
                bot.delete_message(message.chat.id,message.id)
                text=message.text.replace('/call ','')
                if len(text)==11:
                    ports=caller.getFreePort()
                    if ports!='abort':
                        caller.doCall(text,ports)
                        db.executeSql('insert into call(UID,tel,port) values({},"{}","{}")'.format(message.chat.id,text,ports),True)

                        sn.send_notify('Добавлен номер '+text,message.chat.id)
                    else:
                        sn.send_notify('Нет портов',message.chat.id)
                else:
                    sn.send_notify('Неверный номер',message.chat.id)

    nocallFlag=False
    @bot.message_handler(commands=['nocall'])
    def nocall(message) :
        if getPermission(message) =='admin':
            global nocallFlag
            bot.delete_message(message.chat.id,message.id)
            if nocallFlag==True:
                for st in siteThreads:
                    st.nocall()
                sn.send_notify('Вызовы с обьявлений  производятся',message.chat.id)
                nocallFlag=False
            else:
                nocallFlag=True
                for st in siteThreads:
                    st.nocall()
                sn.send_notify('Вызовы с обьявлений не производятся',message.chat.id)


    @bot.message_handler(commands=['status'])

    def status(message)  :
        if getPermission(message) in('admin','sysadm'):
            bot.delete_message(message.chat.id,message.id)
            thc=Process.active_count()
            us = len(db.executeSql('select * from users'))
            global nocallFlag
            global stopbot
            msg='Стат\n'+'Кол-во потоков: '+str(thc)+'\nКол-во юзеров: '+str(us)+'\nЗвонки с обьяв: '+str(not nocallFlag)+'\nБот остановлен: '+str(stopbot)

            bot.send_message(message.from_user.id, msg)

    @bot.message_handler(commands=['say'])
    def say(message):




        if getPermission(message) in ('admin','sysadm'):
            bot.delete_message(message.chat.id,message.id)
            text=message.text.replace('/say ','')
    #        bot.edit_message_text(chat_id=message.chat.id,message_id=message.id,text=text)
            sn.send_call(text,message.chat.id)
        else:
            bot.delete_message(message.chat.id,message.id)
            bot.send_message(message.chat.id,'Denied')

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if getPermission(message)=='lock':
             bot.send_message(message.from_user.id, "Закрыто проходите завтра")
        if getPermission(message) in ('user','admin'):
            global nocallFlag
            if message.text[0] in ('+','8'):

                if len(message.text)>5:
                    bot.delete_message(message.chat.id,message.id)

                    if len(message.text)==11:
                        port=caller.getFreePort()
                        print(port)
                        if port!='abort':
                            caller.doCall(message.text,port)
                            db.executeSql(
                                'insert into call(UID,tel,port) values({},"{}","{}")'.format(message.chat.id, message.text,port), True)
                            sn.send_notify('Добавлен номер '+message.text,message.chat.id,message.chat.id)
                        else:
                            sn.send_notify('Нет портов',message.chat.id,message.chat.id)
                    else:
                        sn.send_notify('Неверный номер',message.chat.id,message.chat.id)

            if message.text == "краш":
                print(message)
    #                siteThreads[4].join()
    #
               # bot.send_message(message.from_user.id, "/start - команда начала сканирования объявлений \n /call - команда набора номера \n /task - вывод запущеных процессов")

            if message.text.find('drom') >=0:


                arg={'id':message.chat.id,'nocall':nocallFlag}
    #            bot.delete_message(message.chat.id,message.id)
                bot.delete_message(message.chat.id,message.id)
                search=db.executeSql('select * from search where UID={} and url="{}"'.format(message.chat.id,message.text))
                if len(search)>0:

                    sn.send_notify('Поиск уже есть',message.chat.id,message.text)
                else:
                        sn.send_notify('Добавлен поиск Дром',message.chat.id,message.text)
                        db.executeSql('insert into search(UID,url,refId,pause) values({},"{}","{}","{}")'.format(message.chat.id,message.text,'',''),True)

                        dromth=threads(message.text,'d',arg)
                        dromth.daemon=True
                        dromth.start()
                        siteThreads.append(dromth)



            if message.text.find('avito') >=0:

                arg={'id':message.chat.id,'nocall':nocallFlag}
                bot.delete_message(message.chat.id,message.id)
                search=db.executeSql('select * from search where UID={} and url="{}"'.format(message.chat.id,message.text))
                if len(search) > 0:

                    sn.send_notify('Поиск уже есть', message.chat.id, message.text)

                else:
                    sn.send_notify('Добавлен поиск Авито',message.chat.id,message.text)
                    db.executeSql('insert into search(UID,url,refId,pause) values({},"{}","{}","{}")'.format(message.chat.id,message.text,'',''),True)
                    thradavito=threads(message.text,'a',arg)
                    thradavito.daemon=True
                    thradavito.start()
                    siteThreads.append(thradavito)


            if message.text.find('youla') >=0:

                arg={'id':message.chat.id,'nocall':nocallFlag}
                bot.delete_message(message.chat.id,message.id)
                search=db.executeSql('select * from search where UID={} and url="{}"'.format(message.chat.id,message.text))
                if len(search) > 0:
                    sn.send_notify('Поиск уже есть', message.chat.id, message.text)

                else:
                    sn.send_notify('Добавлен поиск Юла',message.chat.id,message.text)
                    db.executeSql('insert into search(UID,url,refId,pause) values({},"{}","{}","{}")'.format(message.chat.id,message.text,'',''),True)
                    thradu=threads(message.text,'u',arg)
                    thradu.daemon=True
                    thradu.start()
                    siteThreads.append(thradu)







    @bot.callback_query_handler(func=lambda call: call.data.find('erase_task')>=0)
    def callback_worker(call):
        global select_task
        if call.data == "erase_task":
            try:
                caller.calls[select_task].stop()

                caller.calls.pop(select_task)
                db.executeSql('delete from call where tel="{}"'.format(db.executeSql('select tel from call where UID={}'.format(call.message.chat.id),True)[select_task][1]))

                bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text='Телефон удален')
            except:
                bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text='Телефон удален')
                db.executeSql('delete from call where tel="{}"'.format(db.executeSql('select tel from call where UID={}'.format(call.message.chat.id),True)[select_task][1]))


        #if call.data == "pause_task":
    @bot.callback_query_handler(func=lambda call: call.data=='erase_search')
    def eraseSearch(call):
        global select_task
        if call.data == "erase_search":


            try:

                siteThreads[select_task].stop()
                siteThreads.pop(select_task)

                search=db.executeSql('select * from search where UID={}'.format(call.message.chat.id))
                db.executeSql('delete from search where UID={} and url="{}"'.format(call.message.chat.id,search[select_task][1]),True)
                db.executeSql('delete from sales where UID={} and ref="{}"'.format(call.message.chat.id,search[select_task][1]),True)

                bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text='Поиск удален')

            except:

                bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text='Поиск удален')
                search = db.executeSql('select * from search where UID={}'.format(call.message.chat.id))
                db.executeSql('delete from search where UID={} and url="{}"'.format(call.message.chat.id, search[select_task][1]),True)
                db.executeSql('delete from sales where UID={} and ref="{}"'.format(call.message.chat.id, search[select_task][1]),True)
    @bot.callback_query_handler(func=lambda call: call.data == 'erase_user' )
    def delUs(call):
        global select_task
        db.executeSql('delete from users where UID={}'.format(db.executeSql('select * from users')[select_task][0]),True)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text='Пользователь удален')
    @bot.callback_query_handler(func=lambda call: call.data == 'mute_user' )
    def muteUs(call):
        pass
    @bot.callback_query_handler(func=lambda call: call.data == 'change_user' )
    def changeUs(call):
        pass
    @bot.callback_query_handler(func=lambda call: call.data.find('ref')==0)
    def refUs(call):
        global select_us
        global usrList
        global select_task
        select_us=getRefUsNum(call.data)
        users=db.executeSql('select * from users where UID!={}'.format(call.message.id))
        search=db.executeSql('select * from search where UID={}'.format(call.message.id))
        if users[select_us] in search[select_task][2].split('@'):
            db.executeSql('update search set refId="{}" where UID={} and url="{}"'.format(
                search[select_task][2].replace(users[select_us][0],''), call.message.id, search[1]), True)
        else:
            db.executeSql('update search set refId="{}" where UID={} and url="{}"'.format(search[select_task][2]+'@'+users[select_us][0],call.message.id,search[1]),True)

        call.data='search'+str(select_task)
        searchTask(call)





    #
    #        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text='Выберете действие')
    #        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.id,reply_markup=keyboard)
    @bot.callback_query_handler(func=lambda call: call.data.find('user')==0)
    def actUs(call):
        global select_task
        select_task=getUsNum(call.data)
        if call.data == 'user'+str(select_task):
            keyboard = types.InlineKeyboardMarkup()
            key_erase = types.InlineKeyboardButton(text='Удалить пользователя', callback_data='erase_user')
            key_mute=types.InlineKeyboardButton(text='Мут пользователя', callback_data='mute_user')
            key_ct = types.InlineKeyboardButton(text='Изменить тип пользователя', callback_data='change_user')
            keyboard.add(key_ct,key_mute,key_erase)
            bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text='Выберете действие')
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.id,reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: call.data.find('search')==0)
    def searchTask(call):
        global select_task
        global usrList
        global indl
        select_task=getSearchNum(call.data)
        i=0
        keyboard = types.InlineKeyboardMarkup()

        if getPermission(call.message) in ('admin','sysadm'):
            for user in db.executeSql('select * from users'):
                ref=db.executeSql('select * from search where UID={}'.format(call.message.chat.id))[select_task][2].split('@')

                if user[0]!=call.message.chat.id:
                    if user[0] in ref:

                        keyboard.add(types.InlineKeyboardButton(text= '\U0000274C '+user["firstName"]), callback_data='ref_user'+str(i))
                        i+=1

                    else:
                        keyboard.add(types.InlineKeyboardButton(text= '\U00002714 '+user["firstName"]), callback_data='ref_user'+str(i))
                        i+=1

    #                bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.id,reply_markup=keyboard)
    #            keyboard = types.InlineKeyboardMarkup()

                if db.executeSql('select * from search where UID={}'.format(call.message.chat.id))[select_task][4]=='':
                    key_mute = types.InlineKeyboardButton(text='\U0001F508',callback_data='mut')

                else:
                    key_mute = types.InlineKeyboardButton(text='\U0001F507',callback_data='mut')

            key_erase = types.InlineKeyboardButton(text='Удалить поиск', callback_data='erase_search')
            try:
                if siteThreads[select_task]._paused==True:
                    key_quite = types.InlineKeyboardButton(text='Возобновить поиск', callback_data='pause_s')
                else:
                    key_quite = types.InlineKeyboardButton(text='Приостановить поиск', callback_data='pause_s')
                keyboard.add(key_quite,key_erase,key_mute)
            except:
                keyboard.add(key_erase)



            bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.id,reply_markup=keyboard)
            '''bot.send_message(call.message.chat.id,'Выберете действие', reply_markup=keyboard)'''
    @bot.callback_query_handler(func=lambda call: call.data=='mut')
    def mut(call):
        global select_task


        call.data='search'+str(select_task)
        if db.executeSql('select * from search where UID={}'.format(call.message.chat.id))[select_task][4]!='':
            db.executeSql('update search  set mute="{}" where UID={} and url="{}"'.format('mute',call.message.chat.id,db.executeSql('select * from search where UID={}'.format(call.message.chat.id))[select_task][1]),True)
        else:
            db.executeSql('update search  set mute="{}" where UID={} and url="{}"'.format('', call.message.chat.id,
                                                                                          db.executeSql(
                                                                                              'select * from search where UID={}'.format(
                                                                                                  call.message.chat.id))[
                                                                                              select_task][1]),True)
        searchTask(call)

    @bot.callback_query_handler(func=lambda call: call.data=='pause_s')
    def pause_s(call):
        global select_task
        if db.executeSql('select * from search where UID={}'.format(call.message.chat.id))[select_task][3]!='':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Поиск возобновлен')

            db.executeSql('update search  set pause="{}" where UID={} and url="{}"'.format('pause',call.message.chat.id,db.executeSql('select * from search where UID={}'.format(call.message.chat.id))[select_task][1]),True)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Поиск приостановлен')
            db.executeSql('update search  set pause="{}" where UID={} and url="{}"'.format('', call.message.chat.id,
                                                                                          db.executeSql(
                                                                                          'select * from search where UID={}'.format(
                                                                                                  call.message.chat.id))[
                                                                                              select_task][1]),True)
            siteThreads[select_task].pause()




        siteThreads[select_task].pause()
    @bot.callback_query_handler(func=lambda call: call.data=='pause_call')
    def pause_task(call):
        if caller.calls[select_task]._paused==True:

            bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text='Звонок возобновлен')

            db.executeSql('update call set pause="" where tel="{}"'.format(db.executeSql('select from call where UID={}'.format(call.message.chat.id))[select_task][1]),True)
            caller.calls[select_task].pause()

        else:
            bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text='Звонок приостановлен')
            db.executeSql('update call set pause="pause" where tel="{}"'.format(db.executeSql('select from call where UID={}'.format(call.message.chat.id))[select_task][1]),True)
            caller.calls[select_task].pause()

    #        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.id,reply_markup=keyboard)
    #@bot.callback_query_handler(func=lambda call: call.data[0]=='t'and call.data[2]=='0')
    #def setTime(call) :
    #    qc.put(call.data)
    @bot.callback_query_handler(func=lambda call: call.data.find('task')>=0)
    def taskCall(call):
        global select_task
        select_task=getTaskNum(call.data)

        keyboard = types.InlineKeyboardMarkup()

        if db.executeSql('select * from call where UID={}'.format(call.message.chat.id))[select_task][3]=='pause':
            key_quite = types.InlineKeyboardButton(text='Удалить задачу', callback_data='erase_task')
            key_pause = types.InlineKeyboardButton(text='Возобновить вызов', callback_data='pause_call')
            keyboard.add(key_quite,key_pause)
        else:
            key_quite = types.InlineKeyboardButton(text='Удалить задачу', callback_data='erase_task')
            key_pause = types.InlineKeyboardButton(text='Приостановить вызов', callback_data='pause_call')
            keyboard.add(key_quite, key_pause)
        bot.send_message(call.message.chat.id,'Выберете действие', reply_markup=keyboard)

        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.id)




except requests.exceptions.ConnectionError:
    print('polling error')
except urllib3.exceptions.ConnectionError:
    print('polling error')

# except Exception:
#    import  logging
#    def excepthook_logger(extype, value, traceback):
#        logging.exception("Oh no! An uncaught exception happened!")
#    # Uncomment to also show the exceptions
#    #sys.__excepthook__(extype, value, traceback)
#    sys.excepthook = excepthook_logger
    # e = sys.exc_info()
    # print(e)
#    log(e,'errors')
#    print(e)
#    log(e.args[0],'errors')
    
#    pass
#finally:
#    
#    with open('searchTask.json', 'w') as f:
#        f.close()