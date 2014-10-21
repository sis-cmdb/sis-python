# -*- coding: utf-8 -*-

import base64
import logging

import http
import endpoint

log = logging.getLogger(__name__)

class Client(object):
    def __init__(self, url, version=1.1, auth_token=None):
        self.version = version
        self.base_uri = '%s/api/v%s' % (url.rstrip('/'), self.version)
        self.auth_token = auth_token

        self._http_handler = http.get_handler()

        # api endpoints
        self.schemas = endpoint.Endpoint('schemas', self)
        self.hooks = endpoint.Endpoint('hooks', self)
        self.hiera = endpoint.Endpoint('hiera', self)
        self.users = endpoint.Endpoint('users', self)

    def entities(self, schema_name):
        return endpoint.Endpoint('entities/%s' % schema_name, self)

    def tokens(self, username):
        return endpoint.Endpoint('users/%s/tokens' % username, self)

    def request(self, request):
        return self._http_handler.request(request)

    def authenticate(self, username, password):
        request = http.Request(
            uri='%s/users/auth_token' % self.base_uri,
            method='POST',
            headers={
                'Authorization': 'Basic %s' % base64.b64encode(
                    '%s:%s' % (username, password)
                )
           }     
        )

        self.auth_token =  self.request(request)['name']
        return True

