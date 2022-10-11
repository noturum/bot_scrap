# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 16:47:14 2021

@author: Admin
"""
import os
import subprocess as s
import time
import shutil as g
import threading as th

def say():
    
    print('hi')
    print('lol')
    thh=th.Thread(target=gg,args=())
    thh.start()
def gg() :
    time.sleep(5)
    g.rmtree('../asst',ignore_errors=True)
def updat(f,df,mod) :
    if mod=='new':
         with open(f, 'wb') as new_file:
            new_file.write(df)
    else:
        print('old')
        
        with open(f, 'wb') as new_file:
            new_file.write(df)
    