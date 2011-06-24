'''
Created on Jun 24, 2011

@author: hupf
'''
from daemon.base import CommandHandler, DefaultCommandHandler

class AnimationCommandHandler(CommandHandler):
    def __init__(self, protocol):
        super(AnimationCommandHandler, self).__init__(protocol)
        self.subprompt = 'animation'
    
    def command_help(self, arguments):
        self.protocol.transport.write('''Commands:
    help                           Display this help text
    list                           List the available animations
    play [name]                    Start playing an animation
    exit                           Exit pixel animation mode
''')
    
    def command_list(self, arguments):
        pass
    
    def command_play(self, arguments):
        pass
    
    def command_exit(self, arguments):
        self.protocol.command_handler = DefaultCommandHandler(self.protocol)
        self.subprompt = None
