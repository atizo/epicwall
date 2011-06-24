'''
Created on Jun 24, 2011

@author: hupf
'''

class CommandHandler(object):
    def __init__(self, protocol):
        self.subprompt = None
        self.protocol = protocol
    
    def handle_command(self, data):
        data = data.strip()
        command = data.split(' ')[0]
        
        arguments = []
        if len(data.split(' ')) > 1:
            arguments = data.split(' ')[1:]
        
        if len(command):
            if hasattr(self, 'command_%s' % command):
                command_func = getattr(self, 'command_%s' % command)
                command_func(arguments)
            else:
                self.protocol.transport.write('Unknown command\n')
        
        self.prompt()
    
    def prompt(self):
        if self.subprompt is None:
            self.protocol.transport.write('$ ')
        else:
            self.protocol.transport.write('%s>$ '% self.subprompt)


class DefaultCommandHandler(CommandHandler):
    def command_help(self, arguments):
        self.protocol.transport.write('''Commands:
    help                           Display this help text
    mode [stream|animation|script] Switch to an mode
    exit                           Close connection
''')
    
    def command_exit(self, arguments):
        self.protocol.transport.loseConnection()
    
    def command_mode(self, arguments):
        if len(arguments) != 1 or arguments[0] not in ('stream', 'animation', 'script'):
            self.protocol.transport.write('''Usage:
    mode stream|animation|script
''')
        else:
            mode = arguments[0]
            self.subprompt = mode
            
            if mode == 'stream':
                #self.protocol.command_handler = StreamCommandHandler(self.protocol)
                self.protocol.transport.write('Not implemented\n')
            elif mode == 'pixel':
                from daemon.anim import AnimationCommandHandler
                self.protocol.command_handler = AnimationCommandHandler(self.protocol)
            elif mode == 'script':
                #self.protocol.command_handler = PixelCommandHandler(self.protocol)
                self.protocol.transport.write('Not implemented\n')
