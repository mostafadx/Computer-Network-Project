
#ftp protocol client side

from socket import *
serverName="2.tcp.eu.ngrok.io"
serverPort=14386
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

msg = ''
msg = clientSocket.recv(1024).decode()
a = True
while msg != "QUIT":
    if a:
      print(msg)
    a = True  
    command = input()
    
    if command.startswith('DWLD'):
        clientSocket.send(command.encode())
        status = clientSocket.recv(2024).decode()
        if status == 'OK':
            port = int(clientSocket.recv(2024).decode())
            print('port: ',port)
            # creating the socket with recieved port
            dataSocket = socket(AF_INET,SOCK_STREAM)
            #connecting to the server
            dataSocket.connect((serverName,port))
            # geting file name
            file_path = command.split(' ')[1]
            # writing the file with while
            with open(file_path,'wb') as f:
                while True:
                    data = dataSocket.recv(2024)
                    if not data:
                        break
                    f.write(data)
            print('file downloaded')
            # print(data.decode())
            f.close()
            dataSocket.close()
        else:
            print(status) 
            a = False   
            continue
    else:
        clientSocket.send(command.encode())
    msg = clientSocket.recv(1024).decode()
clientSocket.close()
