# -*- coding: utf-8 -*-

import requests

from requests.auth import HTTPBasicAuth

from .floods import Floods
from .grids import Grids


class Client(object):

    _base_url = 'https://api.flood.io'

    def __init__(self, auth_token):
        self._session = requests.Session()
        self._session.auth = HTTPBasicAuth(auth_token, '')
        self.floods = Floods(self)
        self.grids = Grids(self)


__all__ = ['Client']
