from socketserver import ThreadingTCPServer, BaseRequestHandler
from threading import Thread
import pickle,datetime,os,chatMisc



messages = []
os.system("cls")
class Echo(BaseRequestHandler):
    
        
    def handle(self):
        #Defining some variables
        #self.temp is a list that will hold the last messages, see send
        self.temp = []

        #self.running is used to terminate the Thread that has send running
        self.running = True

        #These are simply requesting and setting the username from the client
        self.username = self.request.recv(8192)
        self.username = self.username.decode()

        #Starts the thread to keep the messages up to date on the client-side
        Thread(target=self.send).start()
        
        

        #Prints out to the server, where the connection has come from
        #Also prints the alias of the connected user
        print("Got connection from {}:{}".format(self.client_address[0],
                                                 self.client_address[1]))
        print("Username: {}".format(self.username))

        #This is the main loop for receiveing messages from the client
        while True:
            try:
                
                msg = self.request.recv(8192)
            except:
                
                print(self.username+" disconnected from the server")
                break

            #Formatting the message
            msg = "[{} | {}]: {}".format(datetime.datetime.now().strftime("%H:%M:%S"),
                                       self.username,
                                       msg.decode())
            
            messages.append(msg)
            print("Message received from {}: {}".format(self.username,msg))

            
            #This checks if the user wishes to quit from the server
            if msg == "quit":
                break

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

                
if __name__ == "__main__":
    serv = ThreadingTCPServer(("",20000), Echo)
    serv.serve_forever()
