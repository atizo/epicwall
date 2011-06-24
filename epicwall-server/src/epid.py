# -*- coding: utf-8 -*-
#
# epicwall Project
# http://epicwall.ch/
#
# Copyright (c) 2011 see AUTHORS file. All rights reserved.
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
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USAª
#

from commands.base import DefaultCommandHandler
from twisted.internet import reactor, protocol
import glob
import serial
import sys

VERSION = '0.1'
PORT = 5000

def scan_serial_devices():
    """scan for available ports. return a list of device names."""
    return glob.glob('/dev/ttyS*') + glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')

SERIAL_DEVICE = None
print 'Available serial devices:'
for name in scan_serial_devices():
    print name
    if "USB" in name:
        SERIAL_DEVICE = name
if SERIAL_DEVICE:
    print 'Selected serial device:', SERIAL_DEVICE
else:
    print 'No USB serial device found'
    sys.exit()

class EpicwallServerProtocol(protocol.Protocol):
    
    def connectionMade(self):
        self.serial_device = serial.Serial(SERIAL_DEVICE, 115200, timeout=1)
        
        self.transport.write('EPICWALL SERVER %s\n\n' % VERSION)
        
        if self.connected > 1:
            self.transport.write('Another client is already connected, disconnecting.\n')
            self.transport.loseConnection()
        
        self.command_handler = DefaultCommandHandler(self)
        self.command_handler.prompt()
    
    def connectionLost(self, reason):
        pass
    
    def dataReceived(self, data):
        if len(data):
            print 'Received', data
        
        self.command_handler.handle_command(data)

def main():
    factory = protocol.ServerFactory()
    factory.protocol = EpicwallServerProtocol
    reactor.listenTCP(PORT, factory)
    reactor.run()

if __name__ == '__main__':
    main()
