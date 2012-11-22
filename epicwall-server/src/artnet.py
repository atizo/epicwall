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
from ola.ClientWrapper import ClientWrapper
from ola.OlaClient import OLADNotRunningException
from serial import Serial
import settings
import simplejson
import sys
from core.color import correct_rgb


def main():

    serial_device = None

    if len(sys.argv) == 1:
        serial_device = Serial(detect_serial_device(), 115200, timeout=1)
    elif len(sys.argv) == 2:
        serial_device = Serial(sys.argv[1], 115200, timeout=1)

    configfile = open(settings.WALL_CONFIG_FILE, 'r')
    data = simplejson.load(configfile)
    configfile.close()
    w = int(data['w'])
    h = int(data['h'])
    mapping = {}
    for k, v in data['mapping'].items():
        mapping[int(k)] = int(v)

    def dmxdata(data):
        print data

        pindex = 0

        fdata = []

        for y in range(h):
            for x in range(w):
                r = data[pindex * 3]
                g = data[pindex * 3 + 1]
                b = data[pindex * 3 + 2]
                color = correct_rgb((r, g, b))
                fdata.extend([0xFF, mapping[y * w + x]])
                fdata.extend(color)
                pindex += 1

        serial_device.write("".join([chr(v) for v in fdata]))

    universe = 1

    wrapper = None
    try:
        wrapper = ClientWrapper()
    except OLADNotRunningException:
        print "Start olad first"
        sys.exit(1)

    client = wrapper.Client()
    client.RegisterUniverse(universe, client.REGISTER, dmxdata)
    wrapper.Run()

if __name__ == '__main__':
    main()
