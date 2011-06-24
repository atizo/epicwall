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

class StreamCommandHandler(CommandHandler):
    
    def __init__(self, protocol):
        super(StreamCommandHandler, self).__init__(protocol)
        self.subprompt = 'stream'
    
    def command_help(self, arguments):
        self.protocol.transport.write('''Commands:
    help                           Display this help text
    exit                           Exit pixel animation mode
''')
    
    def command_exit(self, arguments):
        self.protocol.command_handler = DefaultCommandHandler(self.protocol)
        self.subprompt = None
