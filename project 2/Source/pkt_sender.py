from socket import *
from binascii import unhexlify
def sendeth(pkt,interface):
  s = socket(AF_PACKET, SOCK_RAW)
  s.bind((interface, 0))
  return s.send(pkt)

def pack(byte_sequence):

  return bytes("".join(map(chr, byte_sequence)),'utf-8')
def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    b.append(0x00)    
    return bytes(b[::-1])


pkt = input('What is your packet content? ')
interface_name = input('Which interface do you want to use? ')
pkt = pkt.replace(' ','')
pkt = unhexlify(pkt)
s = socket(AF_PACKET, SOCK_RAW)
s.bind((interface_name, 0))
s.send(pkt)
print('Sent %d-byte on %s' % (len(pkt), interface_name))
