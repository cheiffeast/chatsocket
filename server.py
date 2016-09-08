from socketserver import ThreadingTCPServer, BaseRequestHandler
from threading import Thread
from time import sleep, strftime
import pickle



messages = []
nusers = 0

class messageServer(BaseRequestHandler):
    
        
    def handle(self):
        global nusers, messages
        #Defining some variables
        #self.temp is a list that will hold the last messages, see send
        self.temp = []
        nusers += 1
        #self.running is used to terminate the Thread that has send running
        self.running = True

        #These are simply requesting and setting the username from the client
        self.username = self.request.recv(8192)
        self.username = self.username.decode()

        #Starts the thread to keep the messages up to date on the client-side
        Thread(target=self.send).start()
        
        

        #Prints out to the server, where the connection has come from
        #Also prints the alias of the connected user
        print("Got connection from {}:{}, using username: {}".format(self.client_address[0],
                                                                     self.client_address[1],
                                                                     self.username))
        

        #This is the main loop for receiveing messages from the client
        while True:
            try:
                msg = self.request.recv(8192)
            except:
                nusers -= 1
                print(self.username+" disconnected from the server")
                break

            #Formatting the message
            formattedmsg = "[{}] {}: {}".format(strftime("%H:%m:%S"),
                                       self.username,
                                       msg.decode())
            
            messages.append(formattedmsg)
            
            #This checks if the user wishes to quit from the server
            if msg.decode() == "quit":
                nusers -= 1
                print(self.username+" disconnected from the server")
                break
            log_messages()
        self.running = False
    def send(self):
        
        #This function keeps the clients up to date
        #Everytime a client sends a message, all clients will be updated
        #This specifies that we will be using the global messages, not local
        global messages
        
        while self.running:
            
            #Checks if the two lists are different lengths
            if len(self.temp) != len(messages):


                
                messages2Send = [msg
                                 for msg in messages
                                 if msg not in self.temp]
                data_string = pickle.dumps(messages2Send)
                self.request.send(data_string)
                
                #This makes the self.temp contain the same items as messages
                #Doing self.temp = messages, seems to refernece messages
                #So whenever messages is updated so is self.temp
                self.temp = [item for item in messages]
            sleep(0.1)

def print_users():
    while True:
        print(("[{}] There are currently {} users connected to this server")
              .format(strftime("%H:%m:%S"), nusers))

        sleep(60)




def log_messages():
    
    with open("previousMsg.txt", "w") as f:
        data_string = "\n".join(messages)
        f.write(data_string)
        
def load_config():
    print("nothing")
        
if __name__ == "__main__":
    try:
        Thread(target = print_users).start()
        serv = ThreadingTCPServer(("",20000), messageServer)
        serv.serve_forever()
    except:
        print("A server is already running, 2 servers can not be ran on the same port")
        sleep(2)
