#!/usr/bin/env python
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

from core.serial import detect_serial_device
from serial import Serial
from twisted.internet import reactor
from twisted.web.server import Site
from web.pages import init_web_root, init_resources
import settings
import sys


def main():
    if len(sys.argv) == 1:
        settings.SERIAL_DEVICE = Serial(detect_serial_device(), 115200, timeout=1)
    elif len(sys.argv) == 2:
        settings.SERIAL_DEVICE = Serial(sys.argv[1], 115200, timeout=1)

    web_root = init_web_root()
    web_factory = Site(web_root)
    init_resources(web_root, settings)
    reactor.listenTCP(settings.WEB_PORT, web_factory)

#    shell_factory = protocol.ServerFactory()
#    shell_factory.protocol = lambda: TelnetTransport(TelnetBootstrapProtocol,
#        insults.ServerProtocol, EpicwallShellProtocol)
#    reactor.listenTCP(settings.SHELL_PORT, shell_factory)

    reactor.run()

if __name__ == '__main__':
    main()
