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
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USAª
#

from core.formats import PPMVideoStore
from tornado.websocket import WebSocketHandler
import simplejson
import tornado.web

ws_cache = None


def wall_settings(settings):
    global ws_cache
    if ws_cache is None:
        configfile = open(settings.WALL_CONFIG_FILE, 'r')
        ws_cache = simplejson.load(configfile)
    return ws_cache


class EpicRequestHandler(tornado.web.RequestHandler):
    def initialize(self, coreconf):
        self.coreconf = coreconf


class LedHandler(EpicRequestHandler):

    def get(self):
        self.write('Post LED address and RGB value')

    def post(self):
        s = wall_settings(self.coreconf)
        sd = self.coreconf.SERIAL_DEVICE
        for led in xrange(int(s['addressstart']), int(s['addressend']) + 1):
            data = [0xFF, led]
            data.extend((0, 0, 0))
            sd.write("".join([chr(v) for v in data]))

        data = [0xFF, int(self.get_argument('ledid'))]
        data.extend((254, 240, 0))
        sd.write("".join([chr(v) for v in data]))

        self.write('ok')


class EchoWebSocket(WebSocketHandler):
    def initialize(self, coreconf, animator):
        self.coreconf = coreconf
        self.animator = animator

    def open(self):
        print "WebSocket opened"
        self.animator.set_websocket(self.ws_connection)

    def on_close(self):
        print "WebSocket closed"


class AnimationHandler(EpicRequestHandler):

    def initialize(self, coreconf, animator):
        self.coreconf = coreconf
        self.animator = animator

    def get(self):
        self.write(simplejson.dumps(self.animator.get_animations()))

    def post(self):
        self.animator.update_animation(simplejson.loads(self.request.body))
        self.write('ok')


class AnimatorHandler(EpicRequestHandler):

    def initialize(self, coreconf, animator):
        self.coreconf = coreconf
        self.animator = animator

    def get(self):
        self.write('Start/Stop animator')

    def post(self):
        if self.get_argument('cmd') == 'play':
            self.animator.play()
        else:
            self.animator.stop()

        self.write('ok')


class ConfigHandler(EpicRequestHandler):

    def get(self):
        # read current settings
        configfile = open(self.coreconf.WALL_CONFIG_FILE, 'r')
        data = simplejson.load(configfile)
        configfile.close()
        self.write(simplejson.dumps(data))

    def post(self):
        global ws_cache
        configfile = open(self.coreconf.WALL_CONFIG_FILE, 'w')
        configobj = simplejson.loads(self.request.body)
        ws_cache = configobj
        simplejson.dump(configobj, configfile, indent=4, sort_keys=True)
        configfile.close()
        self.write('ok')

"""
class PixelAnimation(EpicResource):
    isLeaf = True

    def render_GET(self, request):
        if not hasattr(self, 'animation_store') or self.animation_store is None:
            self.video_store = PPMVideoStore(self.settings.PIXEL_ANIMATIONS_PATH)
        if not hasattr(self, 'player') or self.player is None:
            self.player = SerialFramePlayer(self.settings.SERIAL_DEVICE)

        path_args = filter(lambda part: part != '', request.postpath)
        if len(path_args) > 1:
            return NoResource()
        elif len(path_args) == 0:
            response_data = {
                'animations': self.video_store.list(),
                'playing': self.player.is_playing(),
            }
        else:
            action = path_args[0]
            if action not in ('play', 'stop'):
                return NoResource()

            if action == 'play':
                if len(path_args) != 2:
                    return NoResource()
                print 'Playing pixel animation "%s"...' % path_args[1]
                self.player.play(self.video_store.get_frames(path_args[1]))
            elif action == 'stop':
                self.player.stop()
                print 'Stopped pixel animation.'

        return simplejson.dumps(response_data)
"""
