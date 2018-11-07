#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pynput import keyboard
from pynput.keyboard import Key, Controller
k = Controller()

from pynput.mouse import Button,Controller
m=Controller()

import socket
import json
import re
import time
import _thread

from pyperclip import *

SOCKET_MAX=60000
SEGMENT=10000

# 创建 socket 对象
serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名
host = socket.gethostname()

port = 9999

# 绑定端口号
serversocket.bind(("0.0.0.0", port))

# 设置最大连接数，超过后排队
serversocket.listen(1)

table={
"Key.alt":Key.alt,
"Key.alt_gr":Key.alt_gr,
"Key.alt_l":Key.alt_l,
"Key.alt_r":Key.alt_r,
"Key.backspace":Key.backspace,
"Key.caps_lock":Key.caps_lock,
"Key.cmd":Key.cmd,
"Key.cmd_l":Key.cmd_l,
"Key.cmd_r":Key.cmd_r,
"Key.ctrl":Key.ctrl,
"Key.ctrl_l":Key.ctrl_l,
"Key.ctrl_r":Key.ctrl_r,
"Key.delete":Key.delete,
"Key.down":Key.down,
"Key.end":Key.end,
"Key.enter":Key.enter,
"Key.esc":Key.esc,
"Key.f1":Key.f1,
"Key.f2":Key.f2,
"Key.f3":Key.f3,
"Key.f4":Key.f4,
"Key.f5":Key.f5,
"Key.f6":Key.f6,
"Key.f7":Key.f7,
"Key.f8":Key.f8,
"Key.f9":Key.f9,
"Key.f10":Key.f10,
"Key.f11":Key.f11,
"Key.f12":Key.f12,
"Key.home":Key.home,
"Key.insert":Key.insert,
"Key.left":Key.left,
"Key.menu":Key.menu,
"Key.num_lock":Key.num_lock,
"Key.page_down":Key.page_down,
"Key.page_up":Key.page_up,
"Key.pause":Key.pause,
"Key.print_screen":Key.print_screen,
"Key.right":Key.right,
"Key.scroll_lock":Key.scroll_lock,
"Key.shift":Key.shift,
"Key.shift_l":Key.shift_l,
"Key.shift_r":Key.shift_r,
"Key.space":Key.space,
"Key.tab":Key.tab,
"Key.up":Key.up,
"A":"a",
"B":"b",
"C":"c",
"D":"d",
"E":"e",
"F":"f",
"G":"g",
"H":"h",
"I":"i",
"J":"j",
"K":"k",
"L":"l",
"M":"m",
"N":"n",
"O":"o",
"P":"p",
"Q":"q",
"R":"r",
"S":"s",
"T":"t",
"U":"u",
"V":"v",
"W":"w",
"X":"x",
"Y":"y",
"Z":"z",
")":"0",
"!":"1",
"@":"2",
"#":"3",
"$":"4",
"%":"5",
"^":"6",
"&":"7",
"*":"8",
"(":"9",
"_":"-",
"+":"=",
"{":"[",
"}":"]",
"|":"\\",
":":";",
"'":"\"",
"<":",",
">":".",
"?":"/"
}

mouse_table={
    'Button.left':Button.left,
    'Button.right':Button.right
}

def key_model(data):

    key=''
    if data['key'] in table.keys():
        key=table[data['key']]
    else:
        key=data['key']

    if(data['method']=='press'):
        k.press(key)
    elif(data['method']=='release'):
        k.release(key)
    else:
        print('key-Unknow')
        
        return False

def mouse_model(data):

    if(data['method']=='move'):
        x=data['x']
        y=data['y']
        m.move(x,y)
    elif(data['method']=='press'):
        m.press(mouse_table[data['key']])

    elif(data['method']=='release'):
        m.release(mouse_table[data['key']])

    elif(data['method']=='scroll'):
        dx=data['dx']
        dy=data['dy']
        m.scroll(dx,dy)

    else:
        print('mouse-Unknow')
        
        return False
new=''
def wait_clipboard(data):
    global new

    if(data['is_end']=='false'):
        new+=data['content']
    elif(data['is_end']=='true'):
        new+=data['content']

        copy(new)
        new=''

    else:
        print('wait_clipboard Error')
        return False
            

def data_analysis(msgs):
    datas = json.loads(msgs)

    for data in datas:
        if(data['type'] == 'close'):
            return False

        elif(data['type']=='key'):
            if(key_model(data)==False):
                return False

        elif(data['type']=='mouse'):
            if(mouse_model(data)==False):
                return False

        elif(data['type']=='clipboard'):
            if(wait_clipboard(data)==False):
                return False


        else:
            print('type-Unknow')
            
            return False

s_open=False
def listen_clipboard(s):
    time.sleep(1)
    print("Thread start")
    old=paste()
    while (s_open):
        

        new=paste()
        if(new!=old and new!=''):
            old=new

            length = len(new)

            segment=0
            if(length%SEGMENT==0):
                segment=int(length/SEGMENT)
            else:
                segment=int(length/SEGMENT)+1

            for i in range(segment):

                data = {'type': 'clipboard'}
                if(i+1==segment):
                    data['is_end']='true'
               
                    data['content']=new[SEGMENT*i:SEGMENT*(i+1)]
                else:
                    data['is_end']='false'
               
                    data['content']=new[SEGMENT*i:]

                msg = json.dumps(data)+','
                print(time.strftime("%H:%M:%S    ",time.localtime())+msg)
                msg=msg.encode('utf-8')
                s.send(msg)

                time.sleep(0.01)

        time.sleep(1)

    print("Thread over")


while (True):
    # 建立客户端连接
    clientsocket, addr = serversocket.accept()

    s_open=True

    try:
        _thread.start_new_thread( listen_clipboard, (clientsocket, ) )
    except:
        print ("Error: 无法启动线程")
    

    while (True):

        msgs = clientsocket.recv(SOCKET_MAX).decode('utf-8')
        print(time.strftime("%H:%M:%S    ",time.localtime())+msgs)
        msgs='['+msgs[:-1]+']'
        if(data_analysis(msgs)==False):
            clientsocket.close()
            break

    s_open=False

