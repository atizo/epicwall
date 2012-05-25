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
from core.color import correct_rgb
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


class TestAnimationPlayer(SerialFramePlayer):

    def _play_frame(self, usbd):
        t = self._current_frame / 24.0
        rgb_tuple = None

        if t < 5:
            if t < 0.5:
                rgb_tuple = (255, 0, 0)
            elif t < 1:
                rgb_tuple = (0, 255, 0)
            elif t < 1.5:
                rgb_tuple = (0, 0, 255)
            elif t < 2:
                rgb_tuple = (0, 0, 0)
            elif t < 2.5:
                rgb_tuple = (255, 255, 0)
            elif t < 3:
                rgb_tuple = (0, 255, 255)
            elif t < 3.5:
                rgb_tuple = (255, 0, 255)
            elif t < 4:
                rgb_tuple = (255, 255, 255)
            elif t < 4.5:
                rgb_tuple = (0, 0, 0)
            elif t < 5:
                rgb_tuple = (255, 255, 255)
        elif t >= 5 and t < 5 + 12:
            td = t - 5
            if td < 2:
                val = td / 2.0 * 255.0
                rgb_tuple = (val, 0, 0)
            elif td < 4:
                val = 255 - (td - 2) / 2.0 * 255.0
                rgb_tuple = (val, 0, 0)
            elif td < 6:
                val = (td - 4) / 2.0 * 255.0
                rgb_tuple = (0, val, 0)
            elif td < 8:
                val = 255 - (td - 6) / 2.0 * 255.0
                rgb_tuple = (0, val, 0)
            elif td < 10:
                val = (td - 8) / 2.0 * 255.0
                rgb_tuple = (0, 0, val)
            elif td < 12:
                val = 255 - (td - 10) / 2.0 * 255.0
                rgb_tuple = (0, 0, val)
        elif t >= 5 + 12:
            td = t - (5 + 12)
            total_pixels = float(self._width * self._height)
            if td < total_pixels * 0.25:
                rgb_tuple = (255, 255, 255)
                pixel = int(td / 0.25)
#                print 'pixel:', pixel
                data = [0xFF, pixel]
                data.extend(correct_rgb(rgb_tuple))
                usbd.write("".join([chr(v) for v in data]))
            else:
                # restart animation
                t = self._current_frame = 0

        if t < 5 + 12 and rgb_tuple is not None:
#            print correct_rgb(rgb_tuple)
            for row in range(self._height):
                for column in range(self._width):
                    data = [0xFF, row * self._width + column]
                    data.extend(correct_rgb(rgb_tuple))
                    usbd.write("".join([chr(v) for v in data]))

        self._current_frame += 1

    def play(self):
        self.stop()
        self._current_frame = 0
        self._player = RepeatTimer(0.04, self._play_frame, args=[self.serial_device])
        self._player.start()
