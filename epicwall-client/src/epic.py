# -*- coding: utf-8 -*-
#
# epicwall Project
# http://epicwall.ch/
#
# Copyright (c) 2008-2010 Atizo AG. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#

import random
import socket
import sys
import time

HOST = '127.0.0.1'
PORT = 5000

class EpicwallClient:
    def __init__(self):
        self.s = None
    
    def connect(self, host, port):
        self.s = None
        for res in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                self.s = socket.socket(af, socktype, proto)
            except socket.error, msg:
                self.s = None
                continue
            try:
                self.s.connect(sa)
            except socket.error, msg:
                self.s.close()
                self.s = None
                continue
            break
        
        if self.s is None:
            print 'Could not open socket'
        sys.exit(1)
    
    def send_data(self, data):
        if self.s:
            return self.s.send(data)
        else:
            return False
    
    def receive_data(self, length=1024):
        if self.s:
            return self.s.recv(length)
    
    def disconnect(self):
        if self.s:
            self.s.close()

def main():
    client = EpicwallClient()
    client.connect(HOST, PORT)
    
    data = client.receive_data()
    print 'Received', data
    
    frame = 0
    while(True):
        time.sleep(1)
        dd = [frame, random.randint(20,254), 0x33, random.randint(20,254), 0xFF]
        data = "".join([chr(v) for v in dd])
        client.send_data(data)
        print "Sent", repr(data)
        if frame > 50:
            frame = 0
        else:
            frame += 1
    
    client.disconnect()

if __name__ == '__main__':
    main()
