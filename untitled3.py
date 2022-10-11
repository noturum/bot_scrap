# -*- coding: utf-8 -*-
"""
Created on Sat May  8 19:37:33 2021

@author: Admin
"""
from subprocess import Popen
import subprocess
import inspect, os.path
import time
import send_notify as sn
firstime=True

filename = inspect.getframeinfo(inspect.currentframe()).filename
path     = os.path.dirname(os.path.abspath(filename))
bot_stat=''
#print(path+'\..\Python37\python.exe -m '+path+'/telegrambot.py')
print(path+'\\telegrambot.py')
while True:
    if bot_stat==0 or bot_stat=='' :
        if firstime==False:
            sn.error('Программа завершилась! Перезапскаю поиск')
        std=subprocess.call([path[:-5]+'Python37\python.exe',path+'\\telegrambot.py'],shell=True)
        firstime=False
        bot_stat = std
        
    time.sleep(1)
