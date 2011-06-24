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
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#

from commands.base import CommandHandler, DefaultCommandHandler
from playback.formats import PPMVideoStore
from playback.players import SerialFramePlayer
import os

ANIMATIONS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../animations')

class AnimationCommandHandler(CommandHandler):
    
    def __init__(self, protocol):
        super(AnimationCommandHandler, self).__init__(protocol)
        self.subprompt = 'animation'
        
        self.animation_store = PPMVideoStore(ANIMATIONS_PATH)
        self.player = SerialFramePlayer(self.protocol.serial_device)
    
    def command_help(self, arguments):
        self.protocol.transport.write('''Commands:
    help                           Display this help text
    list                           List the available animations
    play [name]                    Start playing an animation
    stop                           Stop a playing animation
    exit                           Exit pixel animation mode
''')
    
    def command_list(self, arguments):
        self.protocol.transport.write('%s\n' % '\n'.join(self.animation_store.list()))
    
    def command_play(self, arguments):
        if len(arguments) != 1 or arguments[0] not in self.animation_store.list():
            self.protocol.transport.write('Invalid animation name\n')
        else:
            animation_name = arguments[0]
            self.player.play(self.animation_store.get_frames(animation_name))
    
    def command_stop(self, arguments):
        self.player.stop()
    
    def command_exit(self, arguments):
        self.protocol.command_handler = DefaultCommandHandler(self.protocol)
        self.subprompt = None
