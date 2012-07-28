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
from datetime import datetime
from threading import Timer, Thread, Event
import time
import simplejson
from core.color import correct_rgb
from core.blit import Layer
import numpy
from core.animation.animations import Empty, ANIMATIONS
from core.animation.base import BELEND_MODES


class RepeatTimer(Thread):
    def __init__(self, interval, callable, args=[], kwargs={}):
        Thread.__init__(self)
        # interval_current shows number of milliseconds in currently triggered <tick>
        self.interval_current = interval
        # interval_new shows number of milliseconds for next <tick>
        self.interval_new = interval
        self.callable = callable
        self.args = args
        self.kwargs = kwargs
        self.event = Event()
        self.event.set()
        self.activation_dt = None
        self.__timer = None

    def run(self):
        while self.event.is_set():
            self.activation_dt = datetime.utcnow()
            self.__timer = Timer(self.interval_new,
                                          self.callable,
                                          self.args,
                                          self.kwargs)
            self.interval_current = self.interval_new
            self.__timer.start()
            self.__timer.join()

    def cancel(self):
        self.event.clear()
        if self.__timer is not None:
            self.__timer.cancel()

    def trigger(self):
        self.callable(*self.args, **self.kwargs)
        if self.__timer is not None:
            self.__timer.cancel()

    def change_interval(self, value):
        self.interval_new = value


class Animator(object):

    def __init__(self, settings):
        self._player = None
        self._w = 0
        self._h = 0
        self._mapping = None
        self._settings = settings
        self._serial_device = self._settings.SERIAL_DEVICE

        self._load_config()

        self._animations = [
                            Empty(self._w, self._h),
                            Empty(self._w, self._h),
                            Empty(self._w, self._h),
                            Empty(self._w, self._h)
                            ]
        self._websockets = {
                            1: None,
                            2: None,
                            3: None,
                            4: None
                            }

    def _load_config(self):
        configfile = open(self._settings.WALL_CONFIG_FILE, 'r')
        data = simplejson.load(configfile)
        configfile.close()
        self._w = int(data['w'])
        self._h = int(data['h'])
        self._mapping = data['mapping']
        r = numpy.ones((self._h, self._w)) * 0.0
        g = numpy.ones((self._h, self._w)) * 0.0
        b = numpy.ones((self._h, self._w)) * 0.0
        a = numpy.ones((self._h, self._w)) * 1.0
        self._bg = Layer([r, g, b, a])

    def _play_frame(self):
        ctime = time.time() * 1000
        frames = [animation.frame(ctime) for animation in self._animations]

        gaga = [numpy.round(band * 255.0) for band in frames[0].getrgba()]
        s1 = []
        for y in range(self._h):
            for x in range(self._w):
                s1.append("rgb(%d,%d,%d)" % (gaga[0][y][x], gaga[1][y][x], gaga[2][y][x]))

        self._websockets[0].write_message(simplejson.dumps(s1))

        outframe = self._bg\
        .blend(frames[3], blendfunc=self._animations[3].get_blend_func())\
        .blend(frames[2], blendfunc=self._animations[2].get_blend_func())\
        .blend(frames[1], blendfunc=self._animations[1].get_blend_func())\
        .blend(frames[0], blendfunc=self._animations[0].get_blend_func())

        n = [numpy.round(band * 255.0).astype(numpy.ubyte) for band in outframe.getrgba()]

        fdata = []

        for y in range(self._h):
            for x in range(self._w):
                r = n[0][y][x]
                g = n[1][y][x]
                b = n[2][y][x]
                color = correct_rgb((r, g, b))
                fdata.extend([0xFF, y * self._w + x])
                fdata.extend(color)

        self._serial_device.write("".join([chr(v) for v in fdata]))

    def play(self):
        self.stop()
        self._load_config()
        self._player = RepeatTimer(0.02, self._play_frame)
        self._player.start()

    def stop(self):
        if self._player:
            self._player.cancel()
            self.player = None

    def is_playing(self):
        return self._player is None or self._player.is_alive()

    def update_animation(self, config):
        layer = config['layer']
        # Check if we have to replace the animation
        if self._animations[layer].name() != config['atype']:
            self._animations[layer] = ANIMATIONS[config['atype']](self._w, self._h)
        anim = self._animations[layer]
        anim.conf(config)

    def get_animations(self):
        anims = []

        for layer, anim in enumerate(self._animations):
            data = anim.json()
            data['layer'] = layer
            data['atypes'] = ANIMATIONS.keys()
            data['blend_modes'] = BELEND_MODES.keys()
            data['atype'] = anim.name()
            anims.append(data)
        return anims

    def set_websocket(self, layer, ws_connection):
        self._websockets[layer] = ws_connection
