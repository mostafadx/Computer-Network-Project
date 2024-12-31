#ftp protocol server
from socket import *
import os
help_msg = '''
Call one of the following functions:
HELP - to get this message
LIST - to list the files in the current directory
PWD - to get the current working directory
CD <dirpath> - to change the current working directory
DWLD <filepath> - to download a file from the server
QUIT - to quit the server
'''
class client_handler(object):

    def is_subdirectory(self,path, subdirectory):
        return subdirectory in path
    def check_path(self,path):
        if self.is_subdirectory(path,self.valid_path) and os.path.exists(path):
            return True
        else:
            return False    
        
    def __init__(self,client,addr):
        self.client = client
        self.addr = addr
        self.dir = ''
        self.valid_path = os.getcwd() + '/dir1'
        os.chdir('dir1')

        print('handling client',addr)
        self.handling()
    def help(self):
        self.client.send(help_msg.encode())
        print('send help')
    def list(self,data=None):
        #list the files in the current directory
        # getting the pwd
        pwd = os.getcwd()
        files = os.listdir(pwd)
        # sending the list of files to client
        list_of_files = ''
        for file in files:
            list_of_files += file + '\n'
        self.client.send(list_of_files.encode())   
    def cd(self,data):
        # change the current working directory
        # getting the path
        path = os.path.abspath(os.path.join(os.getcwd(), data.split(' ')[1]))
        if self.check_path(path):

            try:
                os.chdir(path)
                self.client.send((os.getcwd().split('server/dir1')[1]+'/').encode())
            except Exception as e:
                print(e)
                self.client.send(b'FAIL')
        else:
            self.client.send(b'invalid path')      
    def create_socket_for_file_transfer(self):
        # a random port number between 3000 and 5000
        import random
        port = random.randint(3000,5000)
        # creating a socket
        s = socket(AF_INET,SOCK_STREAM)
        # binding the socket to the port
        s.bind(('127.0.0.1',port))
        # set the socket to listen
        s.listen(5)
        return s,port
    def dwld(self,data):
        # download the file from the server
        # getting the file path
        path = os.path.abspath(os.path.join(os.getcwd(), data.split(' ')[1]))
        if self.check_path(path):
            # checking if the file exists
            if os.path.isfile(path):
                self.client.send(b'OK')
                # creating random socket
                s,port = self.create_socket_for_file_transfer()
                # sending the port number to the client
                self.client.send(str(port).encode())
                # accepting the connection
                connectionSokcet, addr = s.accept()
                print('client connected from ',addr)
                
                # sending the file to the client read until finised
                with open(path,'rb') as f:
                    while True:
                        data = f.read(2024)
                        if not data:
                            break
                        connectionSokcet.send(data)

                
                    
                    

                # print(dataFile.decode())
                
                connectionSokcet.close() 
                self.client.send(b'File sent')   
            else:
                self.client.send(b'FAIL')
        else:
           self.client.send(b'invalid path') 
    def handling(self):
        while True:
            try:
                print('reciveing data')
                data = self.client.recv(2024).decode()
                print(data)
                if data.strip() == 'QUIT':
                    print('closing the connection')
                    self.client.send(b'OUIT')
                    self.client.close()
                    break
                elif data.strip() == 'HELP':
                    self.help()
                elif data.strip() == 'LIST': 
                    self.list()
                elif data.startswith('CD'):
                    self.cd(data)  
                elif data.strip() == 'PWD':
                    self.client.send((os.getcwd().split('server/dir1')[1]+'/').encode())
                elif  data.startswith('DWLD'):
                    # download the file from the server in diffrent socket
                    self.dwld(data)
                else:
                    self.client.send(b'Bad command')

                   
            except Exception as e:
                print(e)
                break
intro_msg= '''
Welcome to the FTP Server.

to get started conncet a client.
server listening on 127.0.0.1:2121

'''

serverPort =12345
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('127.0.0.1',serverPort))
serverSocket.listen(5)
print(intro_msg)
while True:
    connectionSokcet, addr = serverSocket.accept()
    print('client connected from ',addr)
    connectionSokcet.send(help_msg.encode())
    print('waiting for client command')
    client_handler(connectionSokcet,addr)
    connectionSokcet.close()
