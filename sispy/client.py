# -*- coding: utf-8 -*-

import base64
import logging

from . import http
from . import endpoint

LOG = logging.getLogger(__name__)

class Client(object):

    """SIS client"""

    def __init__(self, url, version=1.1, auth_token=None):
        self.version = version
        self.base_uri = '{}/api/v{}'.format(url.rstrip('/'), self.version)
        self.auth_token = auth_token

        # get http handler
        self._http_handler = http.get_handler()

        # api endpoints
        self.schemas = endpoint.Endpoint('schemas', self)
        self.hooks = endpoint.Endpoint('hooks', self)
        self.hiera = endpoint.Endpoint('hiera', self)
        self.users = endpoint.Endpoint('users', self)

    def entities(self, schema_name):
        return endpoint.Endpoint('entities/{}'.format(schema_name), self)

    def tokens(self, username):
        return endpoint.Endpoint('users/{}/tokens'.format(username), self)

    def request(self, request):
        return self._http_handler.request(request)

    def authenticate(self, username, password):
        uri = '{}/users/auth_token'.format(self.base_uri)

        # py3 base64.b64encode expects and returns a byte str
        enc_creds = base64.b64encode(
            '{}:{}'.format(username, password).encode('utf-8')).decode('utf-8')

        headers = { 'Authorization': 'Basic {}'.format(enc_creds) }

        request = http.Request(uri=uri,
                               method='POST',
                               headers=headers)

        self.auth_token =  self.request(request)['name']

        return True

