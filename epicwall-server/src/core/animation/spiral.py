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
from core.blit import Layer
import math


class Spiral(BaseAnimation):

    def __init__(self, w, h):
        super(Spiral, self).__init__(w, h)
        w = self._w
        h = self._h
        xs = 2
        ys = h
        do = True
        total = math.ceil(w * h / 2.0) - h
        cnt = 0
        sround = 1
        pixels1 = []
        pixels2 = []

        for y in range(h):
            pixels1.append((0, y))
            pixels2.append((w - 1, h - y - 1))

        while do and cnt < total:
            limitx = w - sround * 2
            limity = h - sround * 2

            if limitx < 1 and limity < 1:
                do = False

            if sround % 2:
                for x in range(limitx):
                    pixels1.append((xs + x - 1, ys - 1))
                    pixels2.append(((w - 1) - (xs + x - 1), (h - 1) - (ys - 1)))
                    cnt += 1
                    if cnt >= total:
                        break
                xs = xs + x
                ys = ys - 1
                for y in range(limity):
                    pixels1.append((xs - 1, ys - y - 1))
                    pixels2.append(((w - 1) - (xs - 1), (h - 1) - (ys - y - 1)))
                    cnt += 1
                    if cnt >= total:
                        break
                ys = ys - y
                xs = xs - 1
            else:
                for x in range(limitx):
                    pixels1.append((xs - x - 1, ys - 1))
                    pixels2.append(((w - 1) - (xs - x - 1), (h - 1) - (ys - 1)))
                    cnt += 1
                    if cnt >= total:
                        break
                xs = xs - x
                ys = ys + 1

                for y in range(limity):
                    pixels1.append((xs - 1, ys + y - 1))
                    pixels2.append(((w - 1) - (xs - 1), (h - 1) - (ys + y - 1)))
                    cnt += 1
                    if cnt >= total:
                        break

                ys = ys + y
                xs = xs + 1

            sround += 1

        self._pixels1 = pixels1
        self._pixels2 = pixels2

    def animate(self):
        total = len(self._pixels1)
        alpha = 1

        if self._step >= total * 2:
            self._step = 0

        if self._step >= total:
            alpha = 0

        pixel1 = self._pixels1[self._step % total]
        pixel2 = self._pixels2[self._step % total]
        self.setp(pixel1[0], pixel1[1], 0.35, 0.15, 0.9, alpha)
        self.setp(pixel2[0], pixel2[1], 0.17, 0.62, 1, alpha)

        self._step += 1
        return Layer(self._rgba)

    def name(self):
        return 'Spiral'
