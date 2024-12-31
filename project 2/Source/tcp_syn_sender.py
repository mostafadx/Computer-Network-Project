from socket import inet_aton
from binascii import hexlify, unhexlify
from checksum3 import cs
from socket import *
def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    for i in range(54 - len(b)):
        b.append(0x00)    
    return bytes(b[::-1])

def ip(ver,diff,t_len,id,flags,ttl,proto4,checksum,src_ip,dest_ip):
    return (ver + diff + t_len + id + flags + ttl + proto4 + checksum + 
    src_ip + dest_ip).replace(' ','')
def tcp(src_port,dest_port,seq_num,ack,h_len,w_size,checksum,up):
    return (src_port + dest_port + seq_num + ack + h_len 
           + w_size + checksum  + up).replace(' ','')
def ether(dest_mac,src_mac,type):
    return (dest_mac + src_mac + type).replace(' ','')



fd = open('info.txt')
Lines = fd.readlines()
dest_mac = Lines[6][:17]
src_mac = Lines[5][:17]
proto3 = "08 00"
ver = "45"
diff = "00"
t_len = "00 28"
id = "07 c3"
flags = "40 00"
ttl = "40"
proto4 = "06"
cs3 = "00 00"
src_ip = hexlify(inet_aton(Lines[2]))
src_ip = str(src_ip)[2:-1]
dest_ip = hexlify(inet_aton(Lines[0]))
dest_ip = str(dest_ip)[2:-1]
src_port = "%04x"%int(Lines[3])
dest_port = "%04x"%int(Lines[1])
seq_num = "17 49 30 d1"
ack = "00 00 00 00"
h_len = "50 02"
w_size = "72 10"
cs4 = "00 00"
up = "00 00"
unused = '00'

interface0 = Lines[4].strip()
p_ip = ver+diff+t_len+id+flags+ttl+proto4+cs3+src_ip+dest_ip
p_ip = p_ip.replace(' ','')
p_ip = ' '.join(p_ip[i:i+2] for i in range(0,len(p_ip),2))
checksum_ip = cs(p_ip)
p_tcp = src_ip+dest_ip+'00'+ proto4+'00' +'14'+src_port+dest_port+ seq_num +ack+h_len+  w_size+'00 00'+up
p_tcp = p_tcp.replace(' ','')
p_tcp = ' '.join(p_tcp[i:i+2] for i in range(0,len(p_tcp),2))
checksum_tcp = cs(p_tcp) 
pkt = ether(dest_mac,src_mac,proto3) + ip(ver,diff,t_len,id,flags,ttl,proto4,checksum_ip,src_ip,dest_ip) + tcp(src_port,dest_port,seq_num,ack,h_len,w_size,checksum_tcp,up) 
pkt = pkt.replace(' ','')
pkt = unhexlify(pkt)
s = socket(AF_PACKET, SOCK_RAW)
s.bind((interface0, 0))
s.send(pkt)
print('Sent %d-byte on %s' % (len(pkt),interface0))

