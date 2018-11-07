import socket
import time
from pynput import keyboard
from pynput.keyboard import Key, Controller
import json
k=Controller()

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

        msg = json.dumps(data)
        print(time.strftime("%H:%M:%S    ",time.localtime())+msg)
        msg=msg.encode('utf-8')
        s.send(msg)
        s.close()
        #exit
        return False
    else:
        data = {'type': 'key', 'method': 'press'}
        
        data['key']=str(key).replace("'","")

        msg = json.dumps(data)
        print(time.strftime("%H:%M:%S    ",time.localtime())+msg)
        msg=msg.encode('utf-8')
        s.send(msg)
        

def on_release(key):

    if(key==end):
        return False

    data = {'type': 'key', 'method': 'release'}

    data['key']=str(key).replace("'","")

    msg = json.dumps(data)
    print(time.strftime("%H:%M:%S    ",time.localtime())+msg)
    msg=msg.encode('utf-8')
    s.send(msg)


with keyboard.Listener(
    on_press = on_press,
    on_release = on_release) as listener:
    listener.join()