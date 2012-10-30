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


class EpicText(BaseAnimation):

    def __init__(self, w, h):
        super(EpicText, self).__init__(w, h)
        # Works for 5px height only
        if h is not 5:
            raise AttributeError('Wall have to be 5 units high')

        self._text = [
                      [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0],
                      [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
                      [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0],
                      [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
                      [1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1],
                      ]
        self._text_len = len(self._text[0])
        self._step = -self._w

    def animate(self):
        self.clear(1, 1, 1, 0)

        self._step

        for x in range(self._w):
            for y in range(self._h):
                tindex = x + self._step
                if tindex < self._text_len\
                and tindex >= 0\
                and self._text[y][tindex]:
                    self.setp(x, y, 0.24 + tindex * 0.011, 0, 1 - tindex * 0.011, 1)

        if self._step < self._text_len:
            self._step = self._step + 1
        else:
            self._step = -self._w

        return Layer(self._rgba)

    def name(self):
        return 'Epic Text'
