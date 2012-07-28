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

from core.animator import Animator
from core.serial import detect_serial_device
from serial import Serial
from tornado import ioloop, web
from web.handlers import ConfigHandler, LedHandler, AnimationHandler, \
    EchoWebSocket, AnimatorHandler
import os
import settings
import signal
import sys


def main():
    if len(sys.argv) == 1:
        settings.SERIAL_DEVICE = Serial(detect_serial_device(), 115200, timeout=1)
    elif len(sys.argv) == 2:
        settings.SERIAL_DEVICE = Serial(sys.argv[1], 115200, timeout=1)

    animator = Animator(settings)

    def signal_handler(signal, frame):
        animator.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    routes = [
        (r"/static/(.*)", web.StaticFileHandler,
         {"path": os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'web/static')}),
        (r"/configuration/", ConfigHandler, dict(coreconf=settings)),
        (r"/led/", LedHandler, dict(coreconf=settings)),
        (r"/animation/", AnimationHandler, dict(coreconf=settings, animator=animator)),
        (r"/animator/", AnimatorHandler, dict(coreconf=settings, animator=animator)),
        (r"/stream/", EchoWebSocket, dict(coreconf=settings, animator=animator)),
        (r"/(.*)", web.StaticFileHandler,
         {"path": os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'web/templates/index.html')}),
    ]

    web.Application(routes).listen(settings.WEB_PORT)
    ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
