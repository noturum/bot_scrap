import random

from bs4 import BeautifulSoup
import requests
from requests import exceptions as exc
class Proxy():
    def __init__(self):
        self.lenth = 20
        self.proxy=self.fillproxy()
    def fillproxy(self):
        proxy = []
        tmp=[]
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
        try:
            soup = BeautifulSoup(requests.get(url='https://free-proxy-list.net/', headers=HEADERS).text, 'lxml')


        except exc.RequestException as e:
            print('Проблемы, Хьюстон!(реквесты не идут)')
            print(e)
            return None
        elements = soup.find_all(attrs={'class': 'table table-striped table-bordered'})
        for el in elements:
            for a in el.find('tbody').find_all('tr'):

                if len(proxy) == self.lenth:
                    break
                if a.find_all('td')[4].text=='elite proxy':
                    proxy.append((a.find_all('td')[0].text, a.find_all('td')[1].text))


        for p in proxy:

            try:
                a=requests.get("http://icanhazip.com", proxies={"http": f'{p[0]}:{p[1]}',"https": f'{p[0]}:{p[1]}'}, timeout=2)
            except Exception as x:
                continue
            else:
                print(a.text)
                tmp.append({"http": f'{p[0]}:{p[1]}',"https": f'{p[0]}:{p[1]}'})
        return tmp








