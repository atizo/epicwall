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

from daemon.base import DefaultCommandHandler
from twisted.internet import reactor, protocol

VERSION = '0.1'
PORT = 5000

class EpicwallServerProtocol(protocol.Protocol):
    def connectionMade(self):
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