#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QTextEdit, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import time
import socket
import json

table = {
    16777249: "ctrl",
    16777248: "shift",
    16777252: "caps",
    16777217: "tab",
    16777219: "backspace",
    16777220: "enter",
    16777221: "enter",
    16777216: "esc",
    16777251: "alt",
    16777264: "f1",
    16777265: "f2",
    16777266: "f3",
    16777267: "f4",
    16777268: "f5",
    16777269: "f6",
    16777270: "f7",
    16777271: "f8",
    16777272: "f9",
    16777272: "f10",
    16777273: "f11",
    16777274: "f12",
    16777253: "num",
    16777235: "up",
    16777237: "down",
    16777234: "left",
    16777236: "right",
    16777222: "ins",
    16777223: "del",
    16777232: "home",
    16777233: "end",
    16777238: "pgup",
    16777239: "pgdn"
}

special=['space','left','right','up','down','home','end','pgup','pgdn']


end = Qt.Key_F3


class Listen(QWidget):

    def __init__(self):
        super().__init__()
        self.log = ''
        self.num = 0
        self.caps = 0
        # 创建 socket 对象
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 设置端口号
        port = 9999

        # 连接服务，指定主机和端口
        s.connect(("192.168.3.30", port))

        self.server = s

        self.initUI()

    def initUI(self):

        self.reviewEdit = QTextEdit(self)

        self.reviewEdit.setFixedHeight(130)
        self.reviewEdit.setFixedWidth(230)
        self.reviewEdit.move(10, 10)
        self.reviewEdit.setReadOnly(True)

        self.setGeometry(10, 30, 250, 150)
        self.setWindowTitle('Absolute')
        self.show()

    def keyPressEvent(self, e):
        if (e.key() == end):  # f3
            data = {"type": "close"}
            print("end")

            msg = json.dumps(data).encode('utf-8')
            self.server.send(msg)
            self.server.close()

            self.close()
            return

        data = {'type': 'key', 'method': 'press'}

        t = e.key()
        if (t == Qt.Key_Space):
            t='space'
            
        elif(t < 256):
            t = e.text()
        else:
            t = table[t]

        if t in special:
            self.log+= t+' is can use\n'
            self.reviewEdit.setText(self.log)
            return

        data['key'] = t

        if (self.num < 6):
            self.log += time.strftime("%H:%M:%S    ",
                                      time.localtime())+'press  '+t+'\n'
            self.num += 1
        else:
            self.log = self.log[self.log.find(
                '\n')+1:]+time.strftime("%H:%M:%S    ", time.localtime())+'press  '+t+'\n'

        self.reviewEdit.setText(self.log)

        msg = json.dumps(data).encode('utf-8')
        self.server.send(msg)

    def keyReleaseEvent(self, e):
        if(e == end):
            return
        data = {'type': 'key', 'method': 'release'}

        t = e.key()

        if (t == Qt.Key_Space):
            t='space'

        elif(t < 256):
            t = e.text()
        else:
            t = table[t]

        if t in special:
            msg= ('{"type": "key", "method": "press","key":"'+t+'"}').encode('utf-8')
            self.server.send(msg)

        data['key'] = t

        if (self.num < 6):
            self.log += time.strftime("%H:%M:%S    ",
                                      time.localtime())+'release '+t+'\n'
            self.num += 1
        else:
            self.log = self.log[self.log.find(
                '\n')+1:]+time.strftime("%H:%M:%S    ", time.localtime())+'release '+t+'\n'

        self.reviewEdit.setText(self.log)

        msg = json.dumps(data).encode('utf-8')
        self.server.send(msg)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Listen()
    sys.exit(app.exec_())
