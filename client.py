import socket,pickle,os,time
from threading import Thread
from winsound import Beep




    
#Initalise the socket
s = socket.socket()

#connect to the sever
s.connect(('localhost',20000))
messages = []

#Main function to fetch data from the server
def receive():

    while True:

        #Wait to receive data from the server
        data = s.recv(8192)

        #Deserialize the data from the server 
        data = pickle.loads(data)
        os.system("cls")

        #Print out all the items in data
        for item in data:
            messages.append(item)

        for item in messages:
            print(item)

        #winsound.Beep when a new message is received
        Beep(500,250)
#Asking the user for their username
username = input("Enter your username: ")

#Create the thread to keep receiving data
Thread(target=receive).start()

#Send our username to the server
s.send(username.encode())
time.sleep(0.1)

while True:

    #Ask the user for a message
    msg = input(">>")
    
    if msg == "quit":
        break


    
    s.send(msg.encode())
    time.sleep(0.1)
