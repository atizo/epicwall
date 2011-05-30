# Echo client program
import socket
import sys
import random
import time

HOST = '192.168.1.2'
PORT = 1000
s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except socket.error, msg:
        s = None
        continue
    try:
        s.connect(sa)
    except socket.error, msg:
        s.close()
        s = None
        continue
    break

if s is None:
    print 'could not open socket'
    sys.exit(1)

data = s.recv(1024)
print 'Received', data

frame = 0

while(True):
    #time.sleep(1)
    dd = [frame, random.randint(20,254), 0x33, random.randint(20,254), 0xFF]
    data = "".join([chr(v) for v in dd])
    s.send(data)
    #print "send", repr(data)
    if frame > 50:
        frame = 0
    else:
        frame += 1

s.close()