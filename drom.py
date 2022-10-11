# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import time
import send_notify as sn
import sys
import json
import requests
import proxy
import dbConnect as db
from requests import exceptions as exc
last_obj=''
curpag=0
def pageFlip(url,coc):
    global curpag
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    if curpag!=0:

        if '?' in url:
            url=url.split('?')
            try:
                soup = BeautifulSoup(requests.get(url=url[0]+'page'+str(curpag)+'/?'+url[1], headers=HEADERS).text,'lxml')
            except exc.RequestException:
                soup = BeautifulSoup(
                    requests.get(url=url[0] + 'page' + str(curpag) + '/?' + url[1], headers=HEADERS,proxies=proxy.getproxy(db.executeSql('select * from setting where param="lastProxy"'))[0][1]).text, 'lxml')
        else:
            try:
                soup = BeautifulSoup(requests.get(url=url, headers=HEADERS).text,
                                     'lxml')
            except exc.RequestException:
                soup = BeautifulSoup(requests.get(url=url, headers=HEADERS,proxies=proxy.getproxy(db.executeSql('select * from setting where param="lastProxy"'))[0][1]).text,
                                     'lxml')

            
    if curpag==0:
        try:
            soup = BeautifulSoup(requests.get(url=url, headers=HEADERS).text,
                                 'lxml')
        except exc.RequestException:
            soup = BeautifulSoup(requests.get(url=url, headers=HEADERS, proxies=
            proxy.getproxy(db.executeSql('select * from setting where param="lastProxy"'))[0][1]).text,
                                 'lxml')

    return soup
findsal=False    
cookies=''
id_ur=''
nocallFlag=''
def sa(url,es,ep,arg,n):
    sal=''
    global last_obj
    global id_ur
    global nocallFlag
    id_ur=arg['id']
    nocallFlag=n
    ic=0
   
    
    global cookies
    global findsal
    global curpag
    cookies=''
    last_obj=''
    while es.isSet()==False :
        
            
        while findsal==False and es.isSet()==False:
            if ep.isSet()==False:
                
                ep.wait()

            
            soup = pageFlip(url,cookies)

            
            jstr=json.loads(soup.find(attrs={"data-drom-module":"bulls-list"}).get('data-drom-module-data'))
            
            for i in jstr['bullList']['bullsData'][0]['bulls']:
                try:
                    if not 'promotionStatus' in i :
                        sal=i['url']
                        findsal=True
                        curpag=0
                       
                        break
                    
                except:
                    print('pass prom stat')
                    
            
            if curpag<=10:
                curpag+=1
            else:
                curpag=0
            
            
        
        if sal != last_obj and last_obj!='' and sal!='' :
            
            if len(t.getSale(id_ur)['sales'])>0:
                ic=0
                for s in t.getSale(id_ur)['sales']:
                    if s['sale']==sal:
                        ic+=1
                if ic>0:
                    pass
                    
                        
                if ic==0:
                        
                    sn.send_notify('Обьявление найдено '+sal,id_ur,url)
                    try:
                        t.addSale(id_ur,sal,url)
                    except:
                        time.sleep(0.5)

            else:
                sn.send_notify('Обьявление найдено '+sal,id_ur,url)
                try:
                        t.addSale(id_ur,sal,url)
                except:
                        time.sleep(0.5)
        print(sal)
        findsal= False      
        last_obj=sal
        time.sleep(15)
        ic=0
        
    

    return 'stoped'









