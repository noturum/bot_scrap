#!/usr/bin/env python
import logging,threading,time
import telegrambot

import PySimpleGUI as sg
logger = logging.getLogger('mymain')

class Bot():
    def __int__(self):
        pass




class ThreadedApp(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def run(self):
        telegrambot.bot.polling(none_stop=True, interval=1)

    def stop(self):
        self._stop_event.set()


class QueueHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)

def make_window(theme):
    sg.theme(theme)
    menu_def = [['Файл', ['Выход']],
                ['Справка', ['О нас']]]
    right_click_menu_def = [[], ['Справка']]


    main_layout = [
        [sg.Text('Статус:'),sg.Text('выключен')],
        [sg.Button('Запустить бота',key='start_bot')]
    ]
    user_layout=[
        [

        ]
    ]
    setting_layout=[
        [

        ]
    ]






    layout = [[sg.MenubarCustom(menu_def, key='-MENU-', font='Courier 15', tearoff=True)]]
    layout += [[sg.TabGroup([[sg.Tab('Процесс', main_layout),
                              sg.Tab('Пользователи', user_layout),
                              sg.Tab('Настройки', setting_layout)
                              ]])]]
    layout[-1].append(sg.Sizegrip())
    window = sg.Window('Бот', layout, right_click_menu=right_click_menu_def,
                       right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0, 0),
                       use_custom_titlebar=True, finalize=True, keep_on_top=True)
    window.set_min_size(window.size)
    return window


def main():
    window = make_window(sg.theme())
    bot_thread=ThreadedApp()
    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit'):
            print("[LOG] Clicked Exit!")
            break
        if event =='start_bot':
            bot_thread.start()



    window.close()
    exit(0)


if __name__ == '__main__':

    sg.theme('dark green 7')

    main()