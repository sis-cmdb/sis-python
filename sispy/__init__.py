# -*- coding: utf-8 -*-

__version__ = (0, 3, 6)

__author__ = 'Anton Gavrik'

import json
import logging

log = logging.getLogger(__name__)

class Response(object):
    """ Represent the client's response.

    Depending on the calling method behaves either like a dictionary 
    for methods returning a single object e.g. .get() or like a list
    for methods returning multiple objects e.g. .fetch_all()
    """
    def __init__(self, result, meta=None):
        self._result = result    
        self._meta = meta 

    def __len__(self):
        return len(self._result)

    def __getitem__(self, key):
        return self._result[key]

    def __setitem__(self, key, value):
        self._result[key] = value

    def __delitem__(self, key):
        del self._result[key]

    def __iter__(self):
        return iter(self._result)

    # "x in Response"
    def __contains__(self, item):
        if item in self._result:
            return True
        else:
            return False
        
    def __str__(self):
        return str(self._result)
 
class Meta(object):
    """ Represents meta data in the clients response.
    """
    def __init__(self, headers):
        """    
        Args:
            headers: dict containing http headers

        Derived attributes:
            .total_count
                is created and is set to the value of 'x-total-count' header 
                if it's present. 
        """           
        self.headers = headers

        if 'x-total-count' in self.headers:
            self.total_count = int(self.headers['x-total-count'])

class Error(Exception):
    """ SIS Error
    """
    def __init__(
        self, error, http_status_code=None, code=None, response_dict={}
    ):
        """
            Args:
                error: string representing error description
                code: string representing error code
                http_status_code: HTTP status code
                response_dict: dictionary representing encoded 
                    http response body 
        """
        self.error = error
        self.http_status_code = http_status_code
        self.code = code
        self.response_dict = response_dict

        super(Error, self).__init__(self.__str__())

    def __repr__(self):
        return (
            'Error(http_status_code="{http_status_code}", '
            'error={error}, code="{code}", '
            'response_dict={response_dict})'.format(
                error=json.dumps(self.error),
                code=self.code,
                http_status_code=self.http_status_code,
                response_dict=json.dumps(str(self.response_dict))
            )
        )

    def __str__(self):
        return self.error

from client import Client

