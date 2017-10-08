#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# epicwall Project
# http://epicwall.ch/
#
# Copyright (c) 2017 see AUTHORS file. All rights reserved.
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

import simplejson

import settings
from core.color import correct_rgb

configfile = open(settings.WALL_CONFIG_FILE, 'r')
config = simplejson.load(configfile)
configfile.close()
w = int(config['w'])
h = int(config['h'])
mapping = {}
for k, v in config['mapping'].items():
    mapping[int(k)] = int(v)


def send(data, serial_device):
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
