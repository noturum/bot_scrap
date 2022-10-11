
from bs4 import BeautifulSoup
import requests
from requests import exceptions as exc
import dbConnect as db
t=[]

def fillproxy():
    proxy=[]
    proxies = {
        "http": "http://marchenko_ns:Yjz,hm2021@nov_proxy.mfnso.local:8080/",
        "https": "http://marchenko_ns:Yjz,hm2021@nov_proxy.mfnso.local:8080/"
    }
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    try:
        soup=BeautifulSoup(requests.get(url='https://free-proxy-list.net/',headers=HEADERS,proxies=proxies).text, 'lxml')
    except exc.RequestException as e:
        print('Проблемы, Хьюстон!(реквесты не идут)')
        print(e)
        return None
    elements=soup.find_all(attrs={'class':'table table-striped table-bordered'})
    for el in elements:
        for a in el.find('tbody').find_all('tr'):
            proxy.append((a.find_all('td')[0].text,a.find_all('td')[1].text))
            if len(proxy)==20:
                return proxy
def checkproxy(proxy):
    for p in proxy:
        try:
            requests.get("https://www.google.com/", proxies={"http": "http://{}:{}".format(p[0],p[1]) }, timeout=3)
        except Exception as x:
            proxy.pop(proxy.index(p))

        if len(db.executeSql('select * from proxy where url="{}" and port="{}"'.format(p[0],p[1]))) >0 :
            continue
        else:
            db.executeSql('insert into proxy(url,port) values("{}","{}")'.format(p[0],p[1]),True)
def getproxy(id):
    p=db.executeSql('select * from proxy where id={}"'.format(id))
    return {"http": "http://{}:{}".format(p[1],p[2]) }

