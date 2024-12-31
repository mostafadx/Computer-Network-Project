import socket
ip = input('What is the Target IP Address? ')
port =  input('Which port do you want to scan? ')
low_port,high_port = port.split('-')
low_port = int(low_port)
high_port = int(high_port)
for port in range(low_port,high_port+1):
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect((ip,port))
        print('Sent TCP SYN packet to port: '+str(port))
        s.close()
    except:
        print('Sent TCP SYN packet to port: '+str(port))
        s.close()
        continue
    finally:
        s.close()
        continue
    break

