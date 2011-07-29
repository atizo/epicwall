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

from jinja2 import Environment, PackageLoader
from twisted.web.resource import Resource
from twisted.web.static import File
import os

env = Environment(loader=PackageLoader('web', 'templates'))

def get_root_page():
    root = Resource()
    root.putChild('', StartPage())
    root.putChild('static', File(os.path.join(os.path.dirname(os.path.abspath(__file__)), './static')))
#    root.putChild('foo', FooPage())
    
    return root

class Page(Resource):
    def _get_base_context(self):
        from epid import VERSION
        c = {
            'version': VERSION,
        }
        return c

class StartPage(Page):
    isLeaf = False
    
    def render_GET(self, request):
        c = self._get_base_context()
        template = env.get_template('start.html')
        return template.render(c).encode("utf-8")

#class FooPage(Page):
#    isLeaf = True
#    
#    def render_GET(self, request):
#        c = self._get_base_context()
#        template = env.get_template('foo.html')
#        return template.render(c).encode("utf-8")
