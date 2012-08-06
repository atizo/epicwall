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
from core.animation.animations import Empty, ANIMATIONS
from core.animation.base import BELEND_MODES
from core.blit import Layer
from core.color import correct_rgb
from tornado.ioloop import PeriodicCallback
import numpy as np
import simplejson
import time


class Animator(PeriodicCallback):

    def __init__(self, settings):
        self._player = None
        self.toggle = False
        self._w = 0
        self._h = 0
        self._mapping = None
        self._websocket = None
        self._settings = settings
        self._serial_device = self._settings.SERIAL_DEVICE

        self._load_config()

        self._animations = [
                            Empty(self._w, self._h),
                            Empty(self._w, self._h),
                            Empty(self._w, self._h),
                            Empty(self._w, self._h)
                            ]

        super(Animator, self).__init__(self._play_frame, 25)

    def _load_config(self):
        configfile = open(self._settings.WALL_CONFIG_FILE, 'r')
        data = simplejson.load(configfile)
        configfile.close()
        self._w = int(data['w'])
        self._h = int(data['h'])
        self._mapping = data['mapping']
        ones = np.ones((self._h, self._w))
        zeros = np.zeros((self._h, self._w))
        self._bg = Layer([zeros, zeros.copy(), zeros.copy(), ones])

    def _play_frame(self):
        ctime = time.time() * 1000
        frames = [animation.frame(ctime) for animation in self._animations]

        if self.toggle:
            # preview layers
            stream = {
                      'previews': []
                      }

            for i, anim in enumerate(self._animations):
                pf = [np.round(band * 255.0) for band in frames[i].getrgba()]
                pixles = []
                for y in range(self._h):
                    for x in range(self._w):
                        pixles.append("rgba(%d,%d,%d,%d)" % (pf[0][y][x], pf[1][y][x], pf[2][y][x], pf[3][y][x]))

                stream['previews'].append(pixles)

            self._websocket.write_message(simplejson.dumps(stream))
            self.toggle = False
        else:
            self.toggle = True

        outframe = self._bg\
        .blend(frames[3], opacity=self._animations[3].opacity,
               blendfunc=self._animations[3].blendmode)\
        .blend(frames[2], opacity=self._animations[2].opacity,
               blendfunc=self._animations[2].blendmode)\
        .blend(frames[1], opacity=self._animations[1].opacity,
               blendfunc=self._animations[1].blendmode)\
        .blend(frames[0], opacity=self._animations[0].opacity,
               blendfunc=self._animations[0].blendmode)

        n = [np.round(band * 255.0).astype(np.ubyte) for band in outframe.getrgba()]

        """
        for y in range(self._h):
            for x in range(self._w):
                stream['final'].append("rgba(%d,%d,%d,%d)" % (n[0][y][x], n[1][y][x], n[2][y][x], n[3][y][x]))
        """

        fdata = []

        for y in range(self._h):
            for x in range(self._w):
                r = n[0][y][x]
                g = n[1][y][x]
                b = n[2][y][x]
                color = correct_rgb((r, g, b))
                fdata.extend([0xFF, self._mapping[y * self._w + x]])
                fdata.extend(color)

        self._serial_device.write("".join([chr(v) for v in fdata]))

    def play(self):
        self.stop()
        self._load_config()
        super(Animator, self).start()

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

    def set_websocket(self, ws_connection):
        self._websocket = ws_connection
