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
import os
import zipfile

class PPMVideoStore(object):
    
    def __init__(self, video_dir):
        self._video_dir = video_dir
        self._videos = {}
        self.scan()
        self._player = None
        
    def _tokenize(self, data):
        for line in data.split('\n'):
            if line[0] != '#':
                for t in line.split():
                    yield t
 
    def _ppm6toframe(self, data):
        t = self._tokenize(data)
        nexttoken = lambda : next(t)
        assert 'P3' == nexttoken(), 'Wrong filetype'
        width, height, maxval = (int(nexttoken()) for i in range(3))        
        bitmap = [range(height) for row in range(width)]
        
        for h in range(height-1, -1, -1):
            for w in range(0, width):
                bitmap[w][h] = [int(nexttoken()) for i in range(3)]
     
        return bitmap
        
    def scan(self):
        self._videos = {}
        file_list = []
        for root, dirs, files in os.walk(self._video_dir):
            for video in files:
                if ".zip" in video.lower():
                    file_list.append(os.path.join(self._video_dir, video))
        
        for video_file in file_list:
            video_name = os.path.basename(video_file).split('.')[0]
            self._videos[video_name] = []
            zf = zipfile.ZipFile(video_file)
            for filename in zf.namelist()[1:]:
                try:
                    data = zf.read(filename)
                except KeyError:
                    print 'ERROR: Did not find %s in zip file' % filename
                else:
                    self._videos[video_name].append(self._ppm6toframe(data))
    
    def get_frames(self, name):
        if self._videos.has_key(name):
            return self._videos[name]
    
    def list(self):
        return self._videos.keys()
    
    def remove(self, name):
        if self._videos.has_key(name):
            del self._videos[name]
