import socket,pickle,os
from threading import Thread
import time
s = socket.socket()
s.connect(('localhost',20000))
def receive():

    while True:
        
        data = s.recv(8192)
        data = pickle.loads(data)
        os.system("cls")
        for item in data:
            print(item)


username = input("Enter your username: ")
Thread(target=receive).start()

s.send(username.encode())
time.sleep(0.1)
while True:
    
    msg = input(">>")

    if not msg:
        break
    s.send(msg.encode())
    time.sleep(0.1)
##    data = s.recv(8192)
##    data = pickle.loads(data)
##    
##    os.system("cls")
##    
##    for item in data:
##        print(item)
