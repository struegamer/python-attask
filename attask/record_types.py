# -*- coding: utf-8 -*-
###############################################################################
# python-foreman-api - Foreman API Python Library
# Copyright (C) 2012 Stephan Adig <sh@sourcecode.de>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
###############################################################################

import sys
import json

OBJCODE_CLASS = {
               'PROJ':'ProjectRecord',
               'OPTASK':'IssueRecord'
               }
class Record(object):
    def __new__(cls, *args, **kwargs):
        if 'raw_data' in kwargs:
            raw_data = kwargs.get('raw_data', None)
            if 'objCode' in raw_data:
                objCode = raw_data.get('objCode')
                if objCode in OBJCODE_CLASS.keys():
                    data = raw_data
                    aa = []
                    kaa = {'data':raw_data}
                    record = eval(OBJCODE_CLASS[objCode])(*aa, **kaa)
                    return record
        return None

class BaseRecord(object):
    def __init__(self, *args, **kwargs):
        self._raw_data = None
        if 'data' in kwargs:
            self._raw_data = kwargs['data']
    def __getattr__(self, attr):
        if attr not in self.__dict__:
            if attr in self._raw_data:
                return self._raw_data[attr]
            return None
        return self.__dict__[attr]
    
    def __repr__(self):
        return json.dumps(self._raw_data)

class ProjectRecord(BaseRecord):
    pass

class IssueRecord(BaseRecord):
    pass