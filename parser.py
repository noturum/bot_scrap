import threading
import time

import bs4
from bs4 import BeautifulSoup as bs
import requests
args={'domain':'https://www.avito.ru','attr':[{'data-marker':'item'},{'class':'iva-item-titleStep'}],'tag':'a'}
class Parser(threading.Thread):
    PAUSE='pause'
    STOP='stop'
    IDLE='idle'
    RUN='run'
    ERROR='error'
    def __init__(self,args,url):
        super().__init__()
        self.url=url
        self.args=args
        self.stop = threading.Event()
        self.pause = threading.Event()
        self.state=None

    def stop(self):
        self.state=self.STOP
        self.pause.set()
        self.stop.set()

    def pause(self):
        if self.state == self.PAUSE:
            self.pause.clear()
            self.state=self.RUN

        else:
            self.pause.set()
            self.state=self.PAUSE

    def run(self):
        self.state=self.RUN
        tmp=None
        while not self.stop.isSet():
            if self.pause.isSet():
                self.pause.wait()
            try:
                soup=bs(requests.get(self.url).text, 'lxml')
            except :
                pass#здесь обработку запроса
                self.state=self.ERROR
                return
            for step in self.args['attr']:
                tmp=soup.find(attrs=step)
            if 'tag' in self.args:
                link=self.args['domain']+tmp.find(self.args['tag']).get('href')
            print(link)
while True:
    headers = {
        'cookie':'MltIuegZN2COuSe=EOFGWsm50bhh17prLqaIgdir1V0kgrvN; u=2xuq75rk.1gc8h8g.1v42xu1s6qy00; v=1681998400; buyer_laas_location=644560; luri=vladivostok; buyer_location_id=644560; abp=1; _gcl_au=1.1.1991880787.1681998418; _ga=GA1.1.2117973978.1681998419; tmr_lvid=652e30cf112e543783cf4dcc07270a5b; tmr_lvidTS=1681998418738; _ym_uid=1681998420246812276; _ym_d=1681998420; _ym_isad=1; f=5.91b0cc4c87cec2ec4b5abdd419952845a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e94f9572e6986d0c624f9572e6986d0c624f9572e6986d0c62ba029cd346349f36c1e8912fd5a48d02c1e8912fd5a48d0246b8ae4e81acb9fa143114829cf33ca746b8ae4e81acb9fa46b8ae4e81acb9fae992ad2cc54b8aa8b175a5db148b56e9bcc8809df8ce07f640e3fb81381f359178ba5f931b08c66a59b49948619279110df103df0c26013a2ebf3cb6fd35a0ac2da10fb74cac1eab268a7bf63aa148d2dc5322845a0cba1aba0ac8037e2b74f92da10fb74cac1eab71e7cb57bbcb8e0f2da10fb74cac1eab2da10fb74cac1eab0df103df0c26013a037e1fbb3ea05095de87ad3b397f946b4c41e97fe93686adecb8388123cde3fbe04c1cd198727a0602c730c0109b9fbbc60ec9d2f66a8631c9fbdd7f5877c6d729aa4cecca288d6bf861d1d271434c50b71a88e8e84832962ebf3cb6fd35a0ac0df103df0c26013a28a353c4323c7a3a140a384acbddd748f37f1e40e74776ec3de19da9ed218fe23de19da9ed218fe2ddb881eef125a8703b2a42e40573ac3c8edd6a0f40cbfd87da3d420d6cca468c; uxs_uid=d43dd270-df81-11ed-8519-b57c5ae0b4f6; ft="9k17cz++evIFwBVcOi8b50BFOOsZB7blUiG7ni6mJGhXeZ4DShpfGH0KEYZZ/YFKuD80Vf/GId4USpOQc2LSZAbroQKltxXMDLKkioqcvRS7sC/J6+ONAeibJN9JxjXGoO5CGw7eLhw7VjDuKhmhMg0XusJf/Dheu/E1lLdhZezDK5PDZbvcjCZ8eLdLLiL3"; dfp_group=8; tmr_detect=0%7C1682000291914; _ym_visorc=b; sx=H4sIAAAAAAAC%2F1TMTW6rMBAH8Lt4zcKff3u4je0Zv7wSUhDgBEXcvatI7QV%2BbwUAlSMagQI8SGIRRxyDrjUyqfGtuhqVv93uvf%2FLW4J%2FyOTuOe5u3stEeV3nUw1K1GiQrE4%2BaX0NKgnrGtFa0dlyqiyFTDW2aknBFPORndDmUlt2NsjHwS3Ko5zdyTp90Wv9LQPBX4MqrgC6xGSz1r5KlcihkgX7UCDykfHsyxwX2U7LvS3B0v58nf9BtCb3ffyRCem6fgIAAP%2F%2FFvTq7w8BAAA%3D; _ga_M29JC28873=GS1.1.1681998418.1.1.1682000570.60.0.0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

    response = requests.get('https://www.avito.ru/vladivostok/bytovaya_elektronika', headers=headers, timeout=10)
    soup = bs(response.text, 'lxml')
    print(soup.text)
    for step in args['attr']:
        tmp=soup.find(attrs=step)
    if 'tag' in args:
        link=args['domain']+tmp.find(args['tag']).get('href')
    print(link)
    time.sleep(10)




