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
try:
    from restkit import BasicAuth
    from restkit.errors import Unauthorized
except ImportError, e:
    print('You didn\'t install python-restkit library')
    print(e)
    sys.exit(1)

from resource import AttaskResource
class AtTaskError(object):
    def __init__(self, message):
        self._message = message
        self._error = json.loads(message)['error']

    @property
    def error(self):
        return self._error

class AtTask(object):
    def __init__(self, attask_url=None, username=None, password=None):
        self._attask = AttaskResource(attask_url)
        self._sessionid = ''
        self._username = username
        self._password = password

    def login(self):
        if self._username is None or self._password is None:
            return False
        try:
            result = self._attask.get('/attask/api/login',
                                      params_dict={'username':self._username,
                                                   'password':self._password})
            if 'sessionID' in result:
                self._sessionid = result['sessionID']
        except Unauthorized, e:
            return AtTaskError(e.message)

    def list(self):
        pass

    def search(self, search=''):
        pass

    def get(self):
        pass

class AtTaskProjects(AtTask):
    def list(self):
        return self._attask.get('/attask/api/proj/')

