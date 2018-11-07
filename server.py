#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pynput import keyboard
from pynput.keyboard import Key, Controller,KeyCode
import socket
import json
import re
import time

k = Controller()

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
"Key.up":Key.up
}
end=0
while (True):
    # 建立客户端连接
    clientsocket, addr = serversocket.accept()

    while (True):
        if(end==1):
            end=0
            break

        msgs = clientsocket.recv(1024).decode('utf-8')
        print(msgs)
        msgs = re.findall('\{[\d\D]+?\}(?!=\")', msgs)

        for msg in msgs:
            if(msg==''):
                break

            print(time.strftime("%H:%M:%S    ",time.localtime())+msg)
        
            data=json.loads(msg)

            if(data['type'] == 'close'):
                clientsocket.close()
                end=1
                break

            elif(data['type']=='key'):
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
                    print('Unknow')
                    clientsocket.close()
                    break

