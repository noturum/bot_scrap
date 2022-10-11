# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 22:46:56 2021

@author: Admin
"""
import task as t

















from subprocess import Popen
import subprocess
import inspect, os.path
import time
import send_notify as sn
firstime=True



point=''
def gui():
    print(' ________    _      _     ______     _____      _______    ')
    print('|___  ___|  | |    | |   | ____ \   |    \ \   / /   \ \   ')
    print('    | |     | |    | |   | |   \ |  | |__/ /  / /     \ \  ')
    print('    | |     | |    | |   | |___| |  | |__| |  | |     | |  ')
    print('    | |     \ \____/ /   | |  \ \   | |  \ \  \ \     / /  ')
    print('    |_|      \______/    |_|   \_\  |____/_/   \_\___/_/   ')
    print('     _______      ______       _______     _ _    _ _          ')
    print('    |  ___\ \    | ____ \     / /   \ \   | | \  / | |         ')
    print('    | |    \ \   | |   \ |   / /     \ \  | |\ \/ /| |         ')
    print('    | |    | |   | |___| |   | |     | |  | | |__| | |         ')
    print('    | |___ / /   | |  \ \    \ \     / /  | |      | |         ')
    print('    |_|___/ /    |_|   \_\    \_\___/ /   |_|      |_|         ')

def refresh():
    global point
    clear()
    if point=='usr':
        users()
    if point=='cmd':
        command()
    if point=='':
        command()
        

def command():
    global point 
    clear()
    point='cmd'
    print('1. Пользователи')
    print('2. Сверить поиски с массивом')
    ans =int(input())
    if ans==1:
        users()
    if ans==2:
        pass
        
def getAnsw(mark,count):
    while mark>count:
        mark =int(input())
    else:
        return mark
        
        
def clear():
    os.system('cls')
    gui()
def users():
    global point
    clear()
    point='usr'
    print('Пользователи'.center(20))
    j= 0
    for a in t.getUser('users')['user']:
        i=a['firstName']
        j+=1
        if a['type']=='admin':
             print(f'{j}. (A) {i}')
        else:
        
            print(f'{j}. {i}')
    print(f'{j+1}. Назад')
    ans =getAnsw(int(input()),j)
    
    

filename = inspect.getframeinfo(inspect.currentframe()).filename
path     = os.path.dirname(os.path.abspath(filename))
bot_stat=''
#print(path+'\..\Python37\python.exe -m '+path+'/telegrambot.py')
#print(path[:-5]+'Python37\python.exe',path+'\\telegrambot.py')
# with Popen([path[:-5]+'Python37\python.exe',path+'\\telegrambot.py'],stdout=subprocess.PIPE) as proc:
#     print(proc.stdout.read())
#std=subprocess.call([path[:-5]+'Python37\python.exe',path+'\\telegrambot.py'],shell=True)
while True:
    refresh()
    
    if bot_stat==0 or bot_stat=='' :
        if firstime==False:
#            sn.error('Программа завершилась! Перезапскаю поиск')
        
            firstime=False
            
        
    time.sleep(8)