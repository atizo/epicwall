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
from __future__ import print_function  # Only needed for Python 2

import argparse
import os
import sys

try:
    import cPickle as pickle
except:
    import pickle

from ola.ClientWrapper import ClientWrapper
from ola.OlaClient import OLADNotRunningException
from serial import Serial

from core.serial import detect_serial_device
from core.wall import send
from settings import CLIPS_DIR
from datetime import datetime

last = 0


def rec(ar):
    if ar.dev:
        serial_device = Serial(ar.dev, 115200, timeout=1)
    else:
        serial_device = Serial(detect_serial_device(), 115200, timeout=1)

    clip_name = ar.clip
    if not clip_name.endswith('.clip'):
        clip_name += '.clip'

    clip = open(os.path.join(CLIPS_DIR, clip_name), 'w')

    def dmxdata(data):
        global last
        if last == 0:
            td = 0
        else:
            td = int((datetime.now() - last).total_seconds() * 1000)

        last = datetime.now()
        pickle.dump({'td': td, 'frm': data}, clip)

        send(data, serial_device)

    universe = 1

    try:
        wrapper = ClientWrapper()
    except OLADNotRunningException:
        print("Start olad first")
        sys.exit(1)

    client = wrapper.Client()
    client.RegisterUniverse(universe, client.REGISTER, dmxdata)
    wrapper.Run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("clip", help="clip name")
    parser.add_argument("--dev", help="serial device (auto-detected if not provided)")
    args = parser.parse_args()
    rec(args)
