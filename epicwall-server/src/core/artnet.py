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
from core.color import correct_rgb
from ola.ClientWrapper import ClientWrapper
from ola.OlaClient import OLADNotRunningException
from threading import Thread
from tornado.ioloop import PeriodicCallback
import simplejson
import sys


class Artnet(Thread):

    def __init__(self, settings):
        self._w = 0
        self._h = 0
        self._mapping = None
        self._settings = settings
        self._serial_device = self._settings.SERIAL_DEVICE

        self._load_config()

        self.wrapper = None
        self.universe = 1

        super(Artnet, self).__init__()

    def _load_config(self):
        configfile = open(self._settings.WALL_CONFIG_FILE, 'r')
        data = simplejson.load(configfile)
        configfile.close()
        self._w = int(data['w'])
        self._h = int(data['h'])
        self._mapping = {}
        for k, v in data['mapping'].items():
            self._mapping[int(k)] = int(v)

    def _dmxdata(self, data):
        pindex = 0

        fdata = []

        for y in range(self._h):
            for x in range(self._w):
                r = data[pindex * 3]
                g = data[pindex * 3 + 1]
                b = data[pindex * 3 + 2]
                color = correct_rgb((r, g, b))
                fdata.extend([0xFF, self._mapping[y * self._w + x]])
                fdata.extend(color)
                pindex += 1

        self._serial_device.write("".join([chr(v) for v in fdata]))

    def run(self):
        if self.wrapper:
            self.wrapper.Stop()

        try:
            self.wrapper = ClientWrapper()
        except OLADNotRunningException:
            print "Start olad first"
            sys.exit(1)

        client = self.wrapper.Client()
        client.RegisterUniverse(self.universe, client.REGISTER, self._dmxdata)

        self._load_config()
        self.wrapper.Run()

    def play(self):
        self.start()

    def stop(self):
        self.wrapper.Stop()
