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
from Queue import Queue, Empty
from threading import Thread
from time import sleep

from pynput import keyboard
from serial import Serial

from core.serial import detect_serial_device
from core.wall import send
from settings import CLIPS_DIR

try:
    import cPickle as pickle
except:
    import pickle

import glob

clips = {}


def load_clip(c):
    clip = open(c, 'r')

    frames = []
    while True:
        try:
            frames.append(pickle.load(clip))
        except (EOFError, pickle.UnpicklingError):
            break
    clip.close()
    return frames


for clp in glob.glob(CLIPS_DIR + "*.clip"):
    clip_name = os.path.basename(clp).split('.')[0]
    clips[clip_name] = load_clip(clp)
    print("Loaded clip: %s" % clip_name)

q = Queue()


def on_release(key):
    if key == keyboard.Key.esc:
        return False
    q.put(key)


def worker(serial_device):
    frames = None
    frm_idx = 0
    while True:
        try:
            key = q.get(block=False)
            try:
                if key.char in clips.keys():
                    frm_idx = 0
                    frames = clips[key.char]
            except AttributeError:
                print('special key {0} pressed'.format(
                    key))
            q.task_done()

        except Empty:
            pass

        if frames:
            if len(frames) <= frm_idx:
                frm_idx = 0
            frm = frames[frm_idx]
            sleep(frm['td'] / 1000.0)
            send(frm['frm'], serial_device)
            frm_idx += 1


def play(ar):
    if ar.dev:
        serial_device = Serial(ar.dev, 115200, timeout=1)
    else:
        serial_device = Serial(detect_serial_device(), 115200, timeout=1)

    t = Thread(target=worker, args=[serial_device])
    t.daemon = True
    t.start()

    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", help="serial device (auto-detected if not provided)")
    args = parser.parse_args()
    play(args)
