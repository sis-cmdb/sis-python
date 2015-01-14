# SIS-PYTHON
Python client library for interacting with the SIS RESTful API.

# Table of Contents
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [API](#api)
  - [Client authentication](#client-authentication)  
  - [Responses](#responses)
  - [Variables & methods](#variables--methods)
- [Error handling](#error-handling)
- [Test API](#test-api)
- [LICENSE](#license)
  
# Dependencies

The client will attempt to use `httplib2` by default, if unavailable it will fall back to `urllib2`. 

**Important:** It is highly recommended to have `httplib2` installed as it may significantly improve the client's performance. 

# Installation

```
sudo python ./setup.py install
```

# Usage

Import the module
```
import sispy
```

Create a SIS client
```python
# my_token is an optional auth token from SIS
client = sispy.Client(url='https://sis.myorg.com', auth_token='my_token')
```

Authenticate
```python
client.authenticate('user1', 'secret')
```

Fetch all entities of a schema
```python
from pprint import pprint

response = client.entities('test_schema').fetch_all()

for item in response:
    pprint(item)
```

Search for entities of a schema
```python
response = client.entities('test_schema').fetch_all(
    query = {
        'q': { 'some_field': 'some_value' },
    }
)
```

Create a schema
```python
content = {
    'name': 'test_schema',

    '_sis': {    
        'owner': 'ops',
    },
    
    'definition': {
        'hostname': 'String',
        'ip_address': 'String'
    }
}

response = client.schemas.create(content)
```

Update a schema
```python
content_updated = {
    'name': 'test_schema',

    '_sis': {
        'owner': 'ops',
    },

    'definition': {
        'serial_number': 'String',
        'hostname': 'String',
        'ip_address': 'String',
        'status': 'String'
    }
}

schema_entry = client.schemas.update('test_schema', content_updated)
```

Search for schemas
```python
response = client.schemas.fetch_all(
    query = {
        'q': { '_sis.owner': 'ops' },
    }
)
```

Fetch all entities belonging to a schema
```python
response = client.entities('test_schema').fetch_all()
```

Get a schema
```python
response = client.schemas.get('test_schema')
```

Delete a schema
```python
response = client.schemas.delete('test_schema')
```

# API

**sispy.Client(url, version=1.1, auth_token=None, http_keep_alive=True)**

* `url` should contain url of the SIS API server
* `version` API version
* `auth_token` is an optional field that is sent in the `x-auth-token` header
* `http_keep_alive` optional, only affects httplib2 handler, if set to False `Connection`: `close` header will be added to all http requests and any opened connections will be forced to close after each request.

## Client authentication

The client may also acquire and use a temporary token to use against the SIS endpoint via the `authenticate` method:
```python
# this method will raise an exception if authentication fails
client.authenticate(user_name, password)
```
On success `client.auth_token` is set to the temporary token acquired.

## Responses

All methods return `sispy.Response()` object that can be iterated over or accessed similar to a dict or a list (depending on the method used).

List-like response
```python
response = client.entities('test_schema').fetch_all()

# iterate over items in the list
for item in response:
    print item

# print the first item of the list
print response[0]
```

Dictionary-like response
```python
response = client.schemas.get('test_schema')

# iterate over fields
for field in response:
    print field

# print value of field 'field1'
print response['field1']
```

`Response.to_dict()` and `Response.to_list()` methods are also available, returning a dict() or a list() object representation respectively.

`Response` object consists of the below attributes, it is discouraged to access them directly (as these might change in the future) but use the access techniqies outlined above.

* `sispy.Response._result` contains decoded http body (either a list or a dict) and can be inspected directly
* `sispy.Response._meta` holds meta data associated with the response
* `sispy.Response._meta.headers` a dictionary of HTTP response headers
* `sispy.Response._meta.total_count` is defined and set to the value of `x-total-count` HTTP header converted to int() if it's present   

## Variables & methods

**sispy.Client.schemas**

**sispy.Client.hooks**

**sispy.Client.hiera**

**sispy.Client.entities(schema_name)**

* `schema_name` : name of the schema

**sispy.Client.tokens(user_name)**

* `user_name` : name of the user

Objects referred/returned by the above all interact with the appropriate endpoints and expose the following interface:

**fetch_page([query])**

This maps to a GET `/` request against the appropriate endpoint.

* query is an optional dictionary that constructs the query string. Keys in the object may include:
  * q : a dictionary specifying the filter
  * limit : the number of items to return
  * offset : offset into the number of objects to return

Returns a dict-like Response where the `Response._meta.total_count` is an integer that is the total number of items in the collection.

**fetch_all([query])**

This calls `fetch_page` multiple times to fetch all items and returns a list-like Response.

**get(id)**

This maps to a GET `/id` request against the approprivate endpoint.

* id : a string representing the ID of the object on the server. For schemas, hooks, and hiera, this is the `name`.  For entities, it is the `_id`.

A dict-like Response representing the object is returned on success.

**create(content)**

This maps to a POST `/` request against the appropriate endpoint.

* content : a valid dictionary or a list of dictionaries conforming to the endpoint specification

The created object as a dict-like Response is returned on success.

In case bulk create returns a Response dict-like object in the form of
```
{
    'errors': [<items>],
    'success': [<items>]
}
```

**update(id, content)**

This maps to a PUT '/id' request against the appropriate v1 endpoint.

* id : a string representing the ID of the object on the server. For schemas, hooks, and hiera, this is the `name`.  For entities, it is the `_id`

* content : a valid dictionary or a list of dictionaries conforming to the endpoint specification

The updated dict-like Response representing the object is returned on success.

**delete(id)**

This maps to a DELETE '/id' request against the appropriate v1 endpoint.

* id : a string representing the ID of the object on the server. For schemas, hooks, and hiera, this is the `name`.  For entities, it is the `_id`

A dict-like Response representing the deleted object is returned on success.

**delete_bulk(query)**

* query is a dictionary that constructs the query string.

Returns a Response dict-like object in the form of
```
{
    'errors': [<items>],
    'success': [<items>]
}
```

# Error handling

An instance of `sispy.Error` is raised if an HTTP request returns a status code above and including 400.

`sispy.Error` has the following attributes that can be inspected:

* error: SIS error text
* code : SIS error code
* http_status_code : HTTP status code
* response_dict : dictionary representing response body json

Handling connection errors is outside of the client's scope.

# Test API

Example of running the unittests:

```python
#!/usr/bin/env python2.7
"""
SIS Python client tests

This needs to be ran multiple times - with httplib2 installed and
without it.
"""

import getpass
import logging
import unittest

from sispy.testsuite import Test

# set up logging
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter(
        '%(asctime)s:%(module)s:'
        '%(levelname)s:%(message)s'
    )
)
logging.getLogger().addHandler(console_handler)
logging.getLogger().setLevel(logging.DEBUG)

username = getpass.getuser()
password = getpass.getpass()

# init Test()
t = Test(
    url='https://sis.myorg.com',
    username=username,
    password=password,
    owner='ops'
)

# run tests
unittest.TextTestRunner().run(t)
```

# LICENSE

This software is licensed under the BSD 3-Clause license.  Please refer to the [LICENSE](LICENSE) for more information.
