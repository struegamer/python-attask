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
import pprint

try:
    from restkit import BasicAuth
    from restkit.errors import Unauthorized
except ImportError, e:
    print('You didn\'t install python-restkit library')
    print(e)
    sys.exit(1)

from resource import AtTaskResource

class AtTaskError(object):
    def __init__(self, message):
        self._message = message
        self._error = json.loads(message)['error']

    @property
    def error(self):
        return self._error

class AtTask(object):
    def __init__(self, attask_url=None, username=None, password=None):
        self._attask_url = attask_url
        self._sessionid = ''
        self._username = username
        self._password = password
        self._attask = AtTaskResource(self._attask_url)
        self._session = AtTaskSession(self._attask)
        self._projects = None
        if self._login():
            self._projects = AtTaskProjects(self._attask, self._session)

    @property
    def attask(self):
        return self._attask

    @property
    def session(self):
        return self._session

    @property
    def projects(self):
        return self._projects

    def _login(self):
        return self._session.login(self._username, self._password)

    def logout(self):
        self._session.logout()



class AtTaskObject(object):
    def __init__(self, attask=None):
        self._attask = attask
        self._pprinter = pprint.PrettyPrinter(indent=4)

    def list(self):
        pass

    def get(self):
        pass

    def search(self):
        pass

    def new(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass


class AtTaskSession(AtTaskObject):
    def __init__(self, attask=None):
        super(AtTaskSession, self).__init__(attask)
        self._session = None

    @property
    def session(self):
        return self._session

    @property
    def session_id(self):
        if self._session is not None and 'sessionID' in self._session:
            return self._session['sessionID']
    @property
    def user_id(self):
        if self._session is not None and 'userID' in self._session:
            return self._session['userID']

    def login(self, username=None, password=None):
        if username is None or password is None:
            return False
        try:
            result = self._attask.get('/attask/api/login',
                                      params_dict={'username':username,
                                                   'password':password})
            self._pprinter.pprint(result)
            if 'data' in result:
                self._session = result['data']
            return True
        except Unauthorized, e:
            return AtTaskError(e.message)
    def logout(self):
        if self._session is not None:
            result = self._attask.get('/attask/api/logout',
                                      params_dict={'sessionID':self.session_id})
            if 'data' in result:
                return result['data']['success']
        return False

class AtTaskProjects(AtTaskObject):
    def __init__(self, attask=None, session=None):
        super(AtTaskProjects, self).__init__(attask)
        self._session = session
        print self._session

    def list(self):
        print self._session.session_id
        result = self._attask.get('/attask/api/project/search',
                                  params_dict={'sessionID':
                                              self._session.session_id, 'map':True})
        self._pprinter.pprint(result)
    def my(self, status='CUR'):
        result = self._attask.get('/attask/api/project/search',
                                  params_dict={
                                               'sessionID':self._session.session_id,
                                               'projectUserIDs':self._session.user_id,
                                               'status':status
                                               })
        # 'assignedTo:ID':self._session.user_id
        self._pprinter.pprint(result)
    def get(self, project_id):
        result = self._attask.get('/attask/api/project/{0}'.format(project_id),
                                  params_dict={'sessionID':
                                               self._session.session_id})
        self._pprinter.pprint(result)
