import struct
import socket

'''
The TCP pseudo header consists of the Source IP Address field, the Destination IP Address field, an Unused field set to 0x00, the Protocol field for TCP 0x06

'''
def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)

def cs_calc(msg):
    s = 0
    for i in range(0, len(msg) - 1, 2):
        w = ord(msg[i]) + (ord(msg[i+1]) << 8)
        s = carry_around_add(s, w)
    return ~s & 0xffff

def cs(data): 
    data = data.split()
    data = list(map(lambda x: int(x,16), data))
    data = str(struct.pack("%dB" % len(data), *data))
    return "%04x" % socket.ntohs(cs_calc(data))