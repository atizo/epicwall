'''
Created on Jun 24, 2011

@author: hupf
'''
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