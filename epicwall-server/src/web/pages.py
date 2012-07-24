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
from core.players import SerialFramePlayer, TestAnimationPlayer
from jinja2 import Environment, PackageLoader
from twisted.web.error import NoResource
from twisted.web.resource import Resource
from twisted.web.static import File
import os
import simplejson

env = Environment(loader=PackageLoader('web', 'templates'))


def init_web_root():
    root = Resource()
    return root


class EpicResource(Resource, object):
    def __init__(self, settings):
        super(EpicResource, self).__init__()
        self.settings = settings


class Led(EpicResource):
    isLeaf = True

    def render_GET(self, request):
        return 'Post LED address and RGB value'

    def render_POST(self, request):
        sd = self.settings.SERIAL_DEVICE
        data = [0xFF, 4]
        data.extend((254, 250, 0))
        data.extend([0xFF, 4])
        data.extend((254, 254, 254))
        sd.write("".join([chr(v) for v in data]))
        return 'ok'


class Configuration(EpicResource):
    isLeaf = True

    def render_GET(self, request):
        # read current settings
        configfile = open(self.settings.WALL_CONFIG_FILE, 'r')
        data = simplejson.load(configfile)
        configfile.close()
        return simplejson.dumps(data)

    def render_POST(self, request):
        configfile = open(self.settings.WALL_CONFIG_FILE, 'w')
        configobj = simplejson.loads(request.content.getvalue())
        simplejson.dump(configobj, configfile, indent=4, sort_keys=True)
        configfile.close()
        return 'ok'


class TestAnimation(EpicResource):
    isLeaf = True

    def render_POST(self, request):
        path_args = filter(lambda part: part != '', request.postpath)
        if len(path_args) != 1:
            return NoResource()

        if not hasattr(self, 'player') or self.player is None:
            self.player = TestAnimationPlayer(self.settings.SERIAL_DEVICE,
                                              width=50, height=1)

        action = path_args[0]
        if action == 'play':
            print 'Playing test animation...'
            self.player.play()
        elif action == 'stop':
            self.player.stop()
            print 'Stopped test animation.'
        else:
            return NoResource()


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


RESOURCES = {
             'animations': PixelAnimation,
             'test': TestAnimation,
             'configuration': Configuration,
             'led': Led
             }


def init_resources(root, settings):
    root.putChild('', File(os.path.join(os.path.dirname(os.path.abspath(__file__)), './templates/index.html')))
    root.putChild('static', File(os.path.join(os.path.dirname(os.path.abspath(__file__)), './static')))

    for resource_name, resource_class in RESOURCES.items():
        root.putChild(resource_name, resource_class(settings))
