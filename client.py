#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import time
from pynput import keyboard,mouse
from pynput.keyboard import Key, Controller
k=Controller()

from pynput.mouse import Button,Controller
m=Controller()

import json
import _thread

from pyperclip import *

default_x=800
default_y=800

scroll_times=40

SOCKET_MAX=60000
SEGMENT=10000

#for exit
end=Key.f3

# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 设置端口号
port = 9999

# 连接服务，指定主机和端口
s.connect(("192.168.3.30", port))


def on_press(key):

    if (key==end):
        data = {"type": "close"}

        msg = json.dumps(data)+','
        print(time.strftime("    %H:%M:%S    ",time.localtime())+msg)
        msg=msg.encode('utf-8')
        s.send(msg)
        s.close()
        #exit
        return False
    else:
        data = {'type': 'key', 'method': 'press'}
        
        data['key']=str(key).replace("'","")

        msg = json.dumps(data)+','
        print(time.strftime("    %H:%M:%S    ",time.localtime())+msg)
        msg=msg.encode('utf-8')
        s.send(msg)
        

def on_release(key):

    if(key==end):
        return False

    data = {'type': 'key', 'method': 'release'}

    data['key']=str(key).replace("'","")

    msg = json.dumps(data)+','
    print(time.strftime("    %H:%M:%S    ",time.localtime())+msg)
    msg=msg.encode('utf-8')
    s.send(msg)

def on_move(x, y):
    data = {'type': 'mouse', 'method': 'move'}
    x=x-default_x
    y=y-default_y

    if(x==0 and y==0):
        return

    data['x']=x
    data['y']=y

    m.position=(default_x,default_y)

    msg = json.dumps(data)+','
    print(time.strftime("    %H:%M:%S    ",time.localtime())+msg)
    msg=msg.encode('utf-8')
    s.send(msg)


def on_click(x, y, button, method):
    data = {'type': 'mouse'}

    if (method):
        data['method']="press"
    else:
        data['method']="release"

    data['key']=str(button)

    msg = json.dumps(data)+','
    print(time.strftime("    %H:%M:%S    ",time.localtime())+msg)
    msg=msg.encode('utf-8')
    s.send(msg)

def on_scroll(x, y, dx, dy):
    data = {'type': 'mouse','method':'scroll'}

    data['dx']=int(dx)  * scroll_times
    data['dy']=int(dy)  * scroll_times
    print(str(int(dx))+'\t'+str(dy))

    msg = json.dumps(data)+','
    print(time.strftime("    %H:%M:%S    ",time.localtime())+msg)
    msg=msg.encode('utf-8')
    s.send(msg)

def listen_mouse():
    with mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll) as listener:
        listener.join()



def wait_clipboard():
    new=''
    while (True):
        msg=s.recv(SOCKET_MAX).decode('utf-8')
        print(time.strftime("    %H:%M:%S    ",time.localtime())+msg)
        data = json.loads(msg[:-1])

        if(data['type']=='clipboard'):
            if(data['is_end']=='false'):
                new+=data['content']
            elif(data['is_end']=='true'):
                new+=data['content']

                copy(new)
                new=''

            else:
                print('wait_clipboard Error')
                break




def main():
    m.position=(default_x,default_y)

    with keyboard.Listener(
        on_press = on_press,
        on_release = on_release) as listener:


        listener.join()

if(__name__=='__main__'):
    
    new=paste()

    length=len(new)

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
        print(time.strftime("    %H:%M:%S    ",time.localtime())+msg)
        msg=msg.encode('utf-8')
        s.send(msg)

        time.sleep(0.01)


    try:
        _thread.start_new_thread( listen_mouse, ( ) )
        _thread.start_new_thread( wait_clipboard, ( ) )
    except:
        print ("Error: 无法启动线程")

    main()