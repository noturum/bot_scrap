# -*- coding: utf-8 -*-
import time
import serial 
import serial.tools.list_ports
import threading
close_port=''
import queue
qd = queue.Queue()
calls=[]
def gsm7bitdecode(f):
   f = ''.join(["{0:08b}".format(int(f[i:i+2], 16)) for i in range(0, len(f), 2)][::-1])
   return ''.join([chr(int(f[::-1][i:i+7][::-1], 2)) for i in range(0, len(f), 7)])
class thCalls(threading.Thread):
    def __init__(self, tel,port):
        threading.Thread.__init__(self)
        self._tel = tel
        self._port=port
        self._stop = threading.Event()
        self._pause = threading.Event()
        self._paused=False
    def pause(self):
            if self._paused==False:
                self._pause.clear()
                self._paused=True
                
            else:
                self._pause.set()
                self._paused=False
    def stop(self):
        self._stop.set()
    def stopped(self): 
        return self._stop.isSet()
    def run(self):
        self._pause.set()
        call(self._tel,self._port,self._stop,self._pause)
def doCall(tel,port):
    
    threadCall=thCalls(tel,port)
    threadCall.daemon=True
    threadCall.start()
    calls.append(threadCall)
def getFreePort():
    mode='duo'
    global CurPort
    CurPort = 0
    duo=[]
    
    ports = serial.tools.list_ports.comports()
    
    if mode=='duo':
        for port in ports:
            try:
                
                if port.description.find('Modem')>0:
                    ph=serial.Serial(port.name,  9600, timeout=0.5)
                    ph.write(b'AT\r\n')
                    s=ph.readlines()
                    
            
                    if len(s)==2:  
                        if s[1]==b'OK\r\n':
                            
                            CurPort=port.name
                            duo.append(port.name)
                            ph.close()
                if len(duo)==2:
                    print(duo)
                    return duo
            except Exception:
                print('1')
                continue
        if len(duo)<2:
            return 'abort'
                    
                    
                    
            
    else:
        for port in ports:
            try:
                if port.description.find('Modem')>0:
                    ph=serial.Serial(port.name,  9600, timeout=0.5)
                    ph.write(b'AT\r\n')
                    s=ph.readlines()  
        
                    if len(s)==2:  
                        if s[1]==b'OK\r\n':
                            CurPort=port.name                   
                            ph.close()
        
                            return port.name 
            except :
                
                continue    
    if CurPort == 0:
        print('Свободных портов нет')
        return 'abort'
def replace(s, char, index):
    return s[:index] + char + s[index +1:]        
def call(num,port,event,ep):
    mode='duo'
    print(num)
    if num[:1]=='8':
        num=replace(num, '+7', 0)
        print(num)
    if len(num)==12: 
        if mode=='duo':
            try:
                recipient = num
                print('номер '+recipient)
                phone = serial.Serial(port[0],  9600, timeout=None)
                phone1 = serial.Serial(port[1],  9600, timeout=None)
                phone.write(b'ATE1 \r')
                phone1.write(b'ATE1 \r')
                print(phone.readline())
                print(phone1.readline())
            except:
                print('модемы пидрят')
                return 'pass'
                  
            
            while  event.isSet()==False :
            
            
                if ep.isSet()==False:
                    phone.write(b'AT+CHUP\r') 
                    phone1.write(b'AT+CHUP\r') 
                    ep.wait()
                phone.write(b'ATD'+recipient.encode() +b'; \r')
                print(phone.readline())
                time.sleep(0.2)
                phone1.write(b'AT+CHUP\r')
                time.sleep(2.8)
                phone1.write(b'ATD'+recipient.encode() +b'; \r')
                print(phone1.readline())
                time.sleep(0.2)
                phone.write(b'AT+CHUP\r') 
                time.sleep(2.8)
                
                
                    
                
                
            
        else:
            recipient = num
            print('номер '+recipient)
            phone = serial.Serial(port,  9600, timeout=None)
            print('llolo')
            phone.write(b'ATE1 \r')
            
            print(phone.readline())
            
            
            while not event.isSet():
                if ep.isSet()==False:
                    phone.write(b'AT+CHUP\r') 
                    print('pause')
                    ep.wait()
                print('loop')
                phone.write(b'ATD'+recipient.encode() +b'; \r\n')
                
                time.sleep(3)
                phone.write(b'AT+CHUP\r\n')
                
                time.sleep(0.5)
   
                
#                if msg.find('t')>=0:
#                    time.sleep(int(msg.replace('t',''))*60)
                
        
        
        if mode=='duo' :
            print('stop duo')
            phone.write(b'AT+CHUP\r') 
            print(phone.readline())
            
            phone1.write(b'AT+CHUP\r')
            print(phone1.readline())
        else:
            phone.write(b'AT+CHUP\r') 
            
       
    else:
        
            
        print('Invalid phone number')
def close_call(num):
    global close_port
    close_port=num

getFreePort()
'''recipient = num
print('номер '+recipient)
phone = serial.Serial(port,  9600, timeout=None)


time.sleep(0.5)
phone.write(b'ATV1 \r')
time.sleep(1)
print(phone.readline())

while not event.isSet():

phone.write(b'ATD'+recipient.encode() +b'; \r')
print(phone.readline())

time.sleep(4.5)
phone.write(b'AT+CHUP\r')
print(phone.readline())
time.sleep(0.5) 
   


phone.write(b'AT+CHUP\r')

print(phone.readline())
print('Вызов завершен '+num)
time.sleep(0.3) 
phone.close()'''
         
