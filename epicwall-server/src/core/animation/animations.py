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
from core.animation.base import BaseAnimation
from core.animation.spiral import Spiral
from core.blit import Layer
from random import randint
import colorsys
from core.animation.etext import EpicText


class Empty(BaseAnimation):

    def animate(self):
        return self._prevframe

    def name(self):
        return 'None'


class RGBCylce(BaseAnimation):

    def animate(self):
        r, g, b = colorsys.hsv_to_rgb(self._step * 0.01, 1, 1)
        self._step += 1
        if self._step >= 100:
            self._step = 0
        self.clear(r, g, b, 1.0)
        return Layer(self._rgba)

    def name(self):
        return 'RGB Cycle'


class RandomPixel(BaseAnimation):

    def animate(self):

        self.clear(0, 0, 0, 0)

        for p in range(5):
            self.setp(randint(0, self._w - 1), randint(0, self._h - 1,), 1, 0, 1, 1)

        return Layer(self._rgba)

    def name(self):
        return 'Random Pixel'


class Strobe(BaseAnimation):

    def animate(self):

        if self._step:
            self.clear(0, 0, 0, 1)
            self._step = 0
        else:
            self.clear(1, 1, 1, 1)
            self._step = 1

        return Layer(self._rgba)

    def name(self):
        return 'Strobe'


class HorizontalBar(BaseAnimation):

    def animate(self):
        self.clear(1, 1, 1, 0)
        if self._step < self._h:
            for x in range(self._w):
                self.setp(x, self._h - self._step - 1, 1, 0.56, 0, 1)
            self._step = self._step + 1
        else:
            self._step = 0

        return Layer(self._rgba)

    def name(self):
        return 'Horizontal Bar'


class VerticalBounce(BaseAnimation):

    def animate(self):
        self.clear(1, 1, 1, 0)

        x = self._step
        if x >= self._w:
            x = self._w * 2 - x - 2
        for y in range(self._h):
            self.setp(x, y, 0, 0.98, 1, 1)
            if x < self._w - 1:
                self.setp(x + 1, y, 0, 0.98, 1, 0.3)
            if x < self._w - 2:
                self.setp(x + 2, y, 0, 0.98, 1, 0.1)
            if x > 0:
                self.setp(x - 1, y, 0, 0.98, 1, 0.3)
            if x > 1:
                self.setp(x - 2, y, 0, 0.98, 1, 0.1)

        if self._step < self._w * 2 - 3:
            self._step = self._step + 1
        else:
            self._step = 0

        return Layer(self._rgba)

    def name(self):
        return 'Vertical Bounce'


ANIMATIONS = {
              '- None -': Empty,
              'RGB Cycle': RGBCylce,
              'Random Pixel': RandomPixel,
              'Spiral': Spiral,
              'Strobe': Strobe,
              'Horizontal Bar': HorizontalBar,
              'Vertical Bounce': VerticalBounce,
              'Epic Text': EpicText,
              }
