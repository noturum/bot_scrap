import threading
import time
from selenium.webdriver.common.keys import Keys
import os
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.common import exceptions as exc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By

import bs4
from bs4 import BeautifulSoup as bs
import requests

args = {'domain': 'https://www.avito.ru', 'attr': [{'data-marker': 'item'}, {'class': 'iva-item-titleStep'}],
        'tag': 'a'}


class Parser():
    PAUSE = 'pause'
    STOP = 'stop'
    IDLE = 'idle'
    RUN = 'run'
    ERROR = 'error'

    def __init__(self, uid=None, args=None):
        super().__init__()
        self.tabs = []
        # self.args=args
        self.stop = threading.Event()
        self.pause = threading.Event()
        self.state = None
        self.driver = self.getDriver(uid)

    def add_tab(self, url):
        self.driver.switch_to.new_window('tab')
        self.tabs.append({'id': self.driver.current_window_handle, 'url': url, 'args': args})

    def parse(self):
        while True:
            for tab in self.tabs:
                self.state = self.RUN
                tmp = None
                while not self.stop.isSet():
                    if self.pause.isSet():
                        self.pause.wait()
                    try:
                        self.driver.switch_to.window(tab['id'])
                        self.driver.get(tab['url'])
                        time.sleep(1000)

                        soup = bs(self.driver.page_source, 'lxml')
                    except Exception as e:

                        pass  # здесь обработку запроса
                        self.state = self.ERROR
                        print(e)
                        time.sleep(100)
                    for step in args['attr']:
                        tmp = soup.find(attrs=step)
                    if 'tag' in args:
                        link = args['domain'] + tmp.find(args['tag']).get('href')
                    print(link)
                    time.sleep(10 / len(self.tabs))

    def getDriver(self, user, headless: bool = True):
        options = webdriver.ChromeOptions()
        options.set_capability(
            "goog:loggingPrefs", {"performance": "ALL"})
        # options.add_argument('--allow-profiles-outside-user-dir')
        # options.add_argument('--enable-profile-shortcut-manager')
        # options.add_argument(r'user-data-dir=.\User')

        # options.add_argument(f'--profile-directory={user}')
        options.add_argument(
            '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
        if headless == True:
            options.add_argument("start-maximized")
            options.add_argument("disable-infobars")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)
        options.add_argument('log-level=3')
        caps = DesiredCapabilities().CHROME

        caps["pageLoadStrategy"] = "none"
        try:
            driver = webdriver.Chrome('chromedriver.exe', desired_capabilities=caps, options=options)
        except exc.SessionNotCreatedException as e:
            print(e)
            exit(0)

        return driver

    def stop(self):
        self.state = self.STOP
        self.pause.set()
        self.stop.set()
        self.driver.close()
        self.driver.quit()

    def pause(self):
        if self.state == self.PAUSE:
            self.pause.clear()
            self.state = self.RUN

        else:
            self.pause.set()
            self.state = self.PAUSE

    def run(self):
        self.add_tab('https://www.avito.ru/novosibirsk/telefony?cd=1')
        self.parse()
        # self.state=self.RUN
        # tmp=None
        # while not self.stop.isSet():
        #     if self.pause.isSet():
        #         self.pause.wait()
        #     try:
        #         soup=bs(requests.get(self.url).text, 'lxml')
        #     except :
        #         pass#здесь обработку запроса
        #         self.state=self.ERROR
        #         return
        #     for step in self.args['attr']:
        #         tmp=soup.find(attrs=step)
        #     if 'tag' in self.args:
        #         link=self.args['domain']+tmp.find(self.args['tag']).get('href')
        #     print(link)

import setting
import requests, json, sys


class Avito():
    def __init__(self, url):
        self.url = url
        self.s=requests.session()
        self.params = self._set_param()
    def _set_param(self):
        if self.url.find('m.') != -1:
            url = self.url
        else:
            url = self.url.replace('www', 'm')
        d=Parser().getDriver('12')
        d.get(url)
        time.sleep(3)
        logs_raw = d.get_log("performance")
        logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
        for log in logs:
            try:
                if log['params']['request']['url'].find('/mav?')!=-1:
                    self.params=dict(log['params']['request']['postData'])
            except:
                continue
    def parse(self):
        res = self.s.get(setting.api, params=self.params)
        a=res.text
        print(res.text)





#Avito('https://www.avito.ru/novosibirsk/telefony/mobile-ASgBAgICAUSwwQ2I_Dc').parse()
from fp.fp import FreeProxy
print(FreeProxy(https=True).get())
#requests.session().get('https://2ip.ru/',proxies={})