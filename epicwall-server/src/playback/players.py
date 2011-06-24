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
from threading import Thread, Event

class RepeatTimer(Thread):
    
    def __init__(self, interval, function, iterations=0, args=[], kwargs={}):
        Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.iterations = iterations
        self.args = args
        self.kwargs = kwargs
        self.finished = Event()
 
    def run(self):
        count = 0
        while not self.finished.is_set() and (self.iterations <= 0 or count < self.iterations):
            self.finished.wait(self.interval)
            if not self.finished.is_set():
                self.function(*self.args, **self.kwargs)
                count += 1

    def cancel(self):
        self.finished.set()


class SerialFramePlayer(object):
    
    def __init__(self, serial_device, width=10, height=5):
        self.serial_device = serial_device
        self._width = width
        self._height = height
        self._player = None
        self._video_length = 0
        self._current_frame = 0
        self._frames = []
    
    def _play_frame(self, usbd):
        if self._current_frame == self._video_length:
            self._current_frame = 0
            
        for row in range(self._height):
            for column in range(self._width):
                data = [0xFF, row * self._width + column]
                data.extend(self._frames[self._current_frame][column][row])
                usbd.write("".join([chr(v) for v in data]))
        
        self._current_frame += 1
    
    def play(self, frames, iterations=0):
        self.stop()
        self._current_frame = 0
        self._video_length = len(frames)
        self._frames = frames
        self._player = RepeatTimer(0.04, self._play_frame, iterations=iterations, args=[self.serial_device])
        self._player.start()
    
    def stop(self):
        if self._player:
            self._player.cancel()
            self.player = None
    
    def is_playing(self):
        return self._player is None or self._player.is_alive()
