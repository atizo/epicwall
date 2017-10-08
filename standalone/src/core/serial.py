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
import glob
import sys

import binascii


def scan_serial_devices():
    """scan for available ports. return a list of device names."""
    return glob.glob('/dev/ttyS*') + glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')


def detect_serial_device():
    serial_device = None
    print 'Available serial devices:'
    for name in scan_serial_devices():
        print name
        if "USB" in name:
            serial_device = name
    if serial_device:
        print 'Selected serial device:', serial_device
    else:
        print 'No USB serial device found'
        sys.exit()

    return serial_device


class Dummy(object):
    @staticmethod
    def write(data):
        print binascii.hexlify(data)
