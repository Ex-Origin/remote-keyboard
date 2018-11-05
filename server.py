#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pynput import keyboard
from pynput.keyboard import Key, Controller
import socket
import json
import re

table = {
    "ctrl": Key.ctrl,
    "shift": Key.shift,
    "caps": Key.caps_lock,
    "tab": Key.tab,
    "backspace": Key.backspace,
    "enter": Key.enter,
    "esc": Key.esc,
    "alt": Key.alt,
    "f1": Key.f1,
    "f2": Key.f2,
    "f3": Key.f3,
    "f4": Key.f4,
    "f5": Key.f5,
    "f6": Key.f6,
    "f7": Key.f7,
    "f8": Key.f8,
    "f9": Key.f9,
    "f10": Key.f10,
    "f11": Key.f11,
    "f12": Key.f12,
    "num": Key.num_lock,
    "up": Key.up,
    "down": Key.down,
    "left": Key.left,
    "right": Key.right,
    "ins": Key.insert,
    "del": Key.delete,
    "home": Key.home,
    "end": Key.end,
    "pgup": Key.page_up,
    "pgdn": Key.page_down,
    "space": Key.space
}

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
end = 0
while (True):
    # 建立客户端连接
    clientsocket, addr = serversocket.accept()

    while (True):
        if(end == 1):
            end = 0
            break

        msg = clientsocket.recv(1024).decode('utf-8')
        msg = re.findall('\{[\d\D]+?\}(?!=\")', msg)
        for v in msg:
            if(v == ''):
                continue
            data = json.loads(v)

            if(data['type'] == 'close'):
                clientsocket.close()
                end = 1
                break
            elif(data['type'] == 'key'):
                key = data['key']
                if(len(key) > 1):
                    key = table[key]

                if(data['method'] == 'press'):
                    k.press(key)
                elif(data['method'] == 'release'):
                    k.release(key)
