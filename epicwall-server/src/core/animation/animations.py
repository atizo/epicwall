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


ANIMATIONS = {
              'None': Empty,
              'RGB Cycle': RGBCylce,
              'Random Pixel': RandomPixel,
              'Spiral': Spiral,
              }
