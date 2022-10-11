# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 22:14:57 2021

@author: Admin
"""
import os
from bs4 import BeautifulSoup
import urllib.request
import json
#import psycopg2

def getTask(name):
    d = json.JSONDecoder()
    x = open(name+'.json','r').read()
    jlist=[]
    while True:
        try:
           j,n = d.raw_decode(x)
           
           jlist.append(j)
        except ValueError:
            break
        x=x[n:]
    return dict( tasks=jlist )

def eraseTask(tel,name):
    with open('tmp.json', 'w') as f:
        f.close()
    tasks = getTask(name)
    for task in tasks['tasks']:
        if task['tel']!=tel :
            with open('tmp.json', 'w') as f:
                json.dump(task,f,ensure_ascii=False)
    os.remove(name+'.json')
    os.rename('tmp.json',name+'.json')




def saveTask(file,url,tel,price,name,port,paus,ref):
    jstr={"url":url,"tel":tel,"price":price,"name":name,'port':port,'stop':paus,'ref':ref}
    with open(file + '.json', 'a') as f:
        json.dump(jstr,f,ensure_ascii=False)
def pauseTask(tel,t,file):
    with open('tmps.json', 'w') as f:
        f.close()
        tasks = getTask(file)
        for task in tasks['tasks']:
            if task['tel']!=tel :
                with open('tmps.json', 'a') as f:
                    json.dump(task,f,ensure_ascii=False)
            else:
                task['stop']=t
                with open('tmps.json', 'a') as f:
                    json.dump(task,f,ensure_ascii=False)

    os.remove(file+'.json')
    os.rename('tmps.json',file+'.json')
def changeTypeTask(url,t,file):
    with open('tmps.json', 'w') as f:
        f.close()
        tasks = getSearchTask(file)
        for task in tasks['searching']:
            if task['url']!=url :
                with open('tmps.json', 'a') as f:
                    json.dump(task,f,ensure_ascii=False)
            else:
                task['stop']=t
                with open('tmps.json', 'a') as f:
                    json.dump(task,f,ensure_ascii=False)

    os.remove(file+'.json')
    os.rename('tmps.json',file+'.json')
def addRef(file,l,uid,ref,mod):
    
    with open('tmps.json', 'w') as f:
        f.close()
        i=0
        tasks = getSearchTask(file)
        for task in tasks['searching']:
            if mod=='add':
                if task['ref'][0]==uid :
                    if i==l and task['ref'][0]==uid: 
                        task['ref'].append(ref)
                    i+=1
                    
            else:
                if task['ref'][0]==uid :
                    if i==l and task['ref'][0]==uid:
                        task['ref'].pop(task['ref'].index(ref))
                    i+=1
            with open('tmps.json', 'a') as f:
                json.dump(task,f,ensure_ascii=False)
        
                
            

    os.remove(file+'.json')
    os.rename('tmps.json',file+'.json')
def addSearchTask(file,url,ref):
    jstr={"url":url,'ref':ref,'stop':'','mute':''}
    with open(file + '.json', 'a') as f:
        json.dump(jstr,f,ensure_ascii=False)
def getSearchTask(name):
    d = json.JSONDecoder()
    x = open(name+'.json','r').read()
    jlist=[]
    while True:
        try:
           j,n = d.raw_decode(x)
           jlist.append(j)
        except ValueError:
            break
        x=x[n:]
    return dict(searching=jlist )

def eraseSearchTask(name,url,ref):
    with open('tmps.json', 'w') as f:
        f.close()
    if url !='all':
        tasks = getSearchTask(name)
    
        for task in tasks['searching']:
    
            if task['url']==url and task['ref'][0]==ref:
                pass
            else:
    
                with open('tmps.json', 'a') as f:
                    json.dump(task,f,ensure_ascii=False)

    os.remove(name+'.json')

    os.rename('tmps.json',name+'.json')
def saveUser(file,id_u,fn,ln,type_u):
    jstr={"id":id_u,'firstName':fn,'lastName':ln,'type':type_u}
    with open(file + '.json', 'a') as f:
        json.dump(jstr,f,ensure_ascii=False)
def getUser(name):
    d = json.JSONDecoder()
    x = open(name+'.json','r').read()
    jlist=[]
    while True:
        try:
           j,n = d.raw_decode(x)
           jlist.append(j)
        except ValueError:
            break
        x=x[n:]
    return dict(user=jlist)
def eraseUser(id_u,name):
    with open('tmps.json', 'w') as f:
        f.close()
    users = getUser(name)
    for user in users['user']:
        if user['id']!=id_u :
            with open('tmps.json', 'w') as f:
                json.dump(user,f,ensure_ascii=False)

    os.remove(name+'.json')

    os.rename('tmps.json',name+'.json')
def changeTypeUser(id_u,type_u,name):
    with open('tmps.json', 'w') as f:
        f.close()
        users = getUser(name)
        for user in users['user']:
            if user['id']!=id_u :
                with open('tmps.json', 'a') as f:
                    json.dump(user,f,ensure_ascii=False)
            else:
                user['type']=type_u
                with open('tmps.json', 'a') as f:
                    json.dump(user,f,ensure_ascii=False)

    os.remove(name+'.json')
    os.rename('tmps.json',name+'.json')
def getLogin(name):
    d = json.JSONDecoder()
    x = open(name+'.json','r').read()
    jlist=[]
    while True:
        try:
           j,n = d.raw_decode(x)
           jlist.append(j)
        except ValueError:
            break
        x=x[n:]
    return dict(login=jlist)
def saveLogin(login,pas,typ):
    jstr={"login":login,"pass":pas,"type":typ}
    with open('login.json', 'a') as f:
        json.dump(jstr,f,ensure_ascii=False)
def removeLogin(log):
    with open('tmps.json', 'a') as f:
        f.close()
    login = getLogin('login')
    for l in login['login']:
        if l['login']!=log :
            with open('tmps.json', 'w') as f:
                json.dump(l,f,ensure_ascii=False)
    os.remove('login.json')
    os.rename('tmps.json','login.json')
def addSale(uid,sale,ref):
    jstr={"sale":sale,"ref":ref}
    if os.path.exists('sales'+str(uid)+'.json')!=True:
        open('sales'+str(uid)+'.json', 'w')
    with open('sales'+str(uid)+'.json', 'a') as f:
        json.dump(jstr,f,ensure_ascii=False)
def getSale(uid):
    d = json.JSONDecoder()
    if os.path.exists('sales'+str(uid)+'.json')!=True:
        open('sales'+str(uid)+'.json', 'w')
    x = open('sales'+str(uid)+'.json','r').read()
    jlist=[]
    while True:
        try:
           j,n = d.raw_decode(x)
           jlist.append(j)
        except ValueError:
            break
        x=x[n:]
    return dict(sales=jlist)
def removeSale(ref,uid):
    with open('tmps.json', 'w') as f:
        f.close()
    sales = getSale(uid)
    for sale in sales['sales']:
        if sale['ref']!=ref :
            with open('tmps.json', 'w') as f:
                json.dump(sale,f,ensure_ascii=False)

    os.remove('sales.json')

    os.rename('tmps.json','sales.json')
def saveLog(com,id_u,time):
    jstr={"command":com,"id":id_u,"time":time}
    with open('log.json', 'a') as f:
        json.dump(jstr,f,ensure_ascii=False)
def getLog():
    d = json.JSONDecoder()
    x = open('log.json','r').read()
    jlist=[]
    while True:
        try:
           j,n = d.raw_decode(x)
           jlist.append(j)
        except ValueError:
            break
        x=x[n:]
    return dict(logs=jlist)
def getCook():
    d = json.JSONDecoder()
    x = open('cook.json','r').read()
    jlist=[]
    while True:
        try:
           j,n = d.raw_decode(x)
           jlist.append(j)
        except ValueError:
            break
        x=x[n:]
    return dict(cook=jlist)
def flipCook():
    tmp=getCook()['cook']
    
    if  len(tmp[0]['cook']) > tmp[0]['lastIndex']:
        tmp[0]['lastIndex']=tmp[0]['lastIndex']+1
    with open('cook.json', 'w') as f:
        json.dump(tmp[0],f,ensure_ascii=False)
def getmute():
    d = json.JSONDecoder()
    x = open('mute.json','r').read()
    jlist=[]
    while True:
        try:
           j,n = d.raw_decode(x)
           jlist.append(j)
        except ValueError:
            break
        x=x[n:]
    return dict(mute=jlist)
def mute(id_chat,url):
    
    with open('tmps.json', 'w') as f:
        f.close()
        
    tasks = getSearchTask('searchTask')
    for task in tasks['searching']:
        
        if task['ref'][0]==id_chat and task['url']==url:
            
            if task['mute']=='':
                
                task['mute']='true'
            else:
                task['mute']=''
            
                
        with open('tmps.json', 'a') as f:
            json.dump(task,f,ensure_ascii=False)
        
                
            

    os.remove('searchTask.json')
    os.rename('tmps.json','searchTask.json')
            
    
def getProxy():
    req = urllib.request.Request('http://www.freeproxylists.net/ru/?pr=HTTPS&s=u')
    
    html = urllib.request.urlopen(req).read()
    print(html)
    soup = BeautifulSoup(html, 'lxml')
    ip= soup.find(attr={'class':'Odd'}).get('a')
    
    print(ip)
    


