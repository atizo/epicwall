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
from core.blit import Layer
from core.blit.blends import multiply, screen, add, subtract, linear_light, \
    hard_light
import numpy

BLEND_MODE_NORMAL = 'normal'
BLEND_MODE_MULTIPLY = 'multiply'
BLEND_MODE_SCREEN = 'screen'
BLEND_MODE_ADD = 'add'
BLEND_MODE_SUB = 'subtract'
BLEND_MODE_LINEAR_LIGHT = 'linear light'
BLEND_MODE_HARD_LIGHT = 'hard light'

BELEND_MODES = {
                BLEND_MODE_NORMAL: None,
                BLEND_MODE_MULTIPLY: multiply,
                BLEND_MODE_SCREEN: screen,
                BLEND_MODE_ADD: add,
                BLEND_MODE_SUB: subtract,
                BLEND_MODE_LINEAR_LIGHT: linear_light,
                BLEND_MODE_HARD_LIGHT: hard_light
                }


class BaseAnimation(object):

    def __init__(self, w, h):
        self._w = int(w)
        self._h = int(h)

        self._speed = 25
        self._blend_mode = BLEND_MODE_NORMAL
        self._hue = 0
        self._colorize = False
        self._brighness = 0
        self._contrast = 0

        self._step = 0
        r = numpy.ones((self._h, self._w)) * 0.0
        g = numpy.ones((self._h, self._w)) * 0.0
        b = numpy.ones((self._h, self._w)) * 0.0
        a = numpy.ones((self._h, self._w)) * 0.0
        self._rgba = [r, g, b, a]
        self._prevframe = Layer(self._rgba)
        self._last_time = 0

    def json(self):
        return {
                 'hue': self._hue,
                 'colorize': self._colorize,
                 'contrast': self._contrast,
                 'brightness': self._brighness,
                 'speed': self._speed,
                 'blend_mode': self._blend_mode,
                 'w': self._w,
                 'h': self._h,
                 }

    def conf(self, data):
        self._hue = int(data['hue'])
        self._colorize = int(data['colorize'])
        self._contrast = int(data['contrast'])
        self._brightness = int(data['brightness'])
        self._speed = int(data['speed'])
        self._blend_mode = data['blend_mode']

    def setp(self, x, y, r, g, b, a):
        self._rgba[0][y][x] = r
        self._rgba[1][y][x] = g
        self._rgba[2][y][x] = b
        self._rgba[3][y][x] = a

    def clear(self, r, g, b, a):
        for x in range(self._w):
            for y in range(self._h):
                self.setp(x, y, r, g, b, a)

    def frame(self, time):
        if time >= self._last_time + 1000 / self._speed:
            self._prevframe = self.animate()
            self._last_time = time
            return self._prevframe
        else:
            return self._prevframe

    def get_blend_func(self):
        return BELEND_MODES[self._blend_mode]
