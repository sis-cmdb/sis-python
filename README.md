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
- [Thread safety](#thread-safety)
- [Error handling](#error-handling)
- [LICENSE](#license)
  
# Dependencies
- Python 2.6+, 3.4+

The client will work using the standard library only, however, if Requests(https://pypi.python.org/pypi/requests/) v2+(must have Session.prepare_request() method) is installed, it will automatically attempt to use it in order to siginificantly improve it's performance.

Check which HTTP library is used:
```
>>> import sispy; print(sispy.http.HTTP_LIB)
requests
```

# Installation

```
sudo python ./setup.py install
```
or via PIP
```
pip install sispy
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
* `http_keep_alive` optional, only affects requests library, when set to False `Connection: close` header will be added to all HTTP requests(see Thread safety paragraph)

## Client authentication

The client may also acquire and use a temporary token to use against the SIS endpoint via the `authenticate` method:
```python
# this method will raise an exception if authentication fails
client.authenticate(user_name, password)
```
On success `client.auth_token` is set to the temporary token acquired.

## Responses

All methods return `sispy.Response()` object that can be iterated over (using `for in`) or accessed similar to a dict or a list (depending on the method used).

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

**update_bulk(content, [query])**

This maps to a PUT `/` request against the appropriate endpoint.

* content : a valid list of dictionaries where each entry contains an update and an `_id` field or a dictionary with an update accompanied with a `query`.
* query : a dictionary that constructs the query string. Entries that match this query will be updated with the dictionary provided by content.

For example:

```python
# List of dictionaries to be updated
updated_entities = [
    {
        "_id": "558481a32bcda71c7b948895",
        "field1": "cat",
        "field2": 4
    },
    {
        "_id": "558481a383cda2b12390ce12",
        "field2": 5
    }
]

# Execute update with bulk_update
client.bulk_update(updated_entities)

# Field to be udpated
update_dict = {
    "field2": 15
}

# Query to select which objects should be updated
update_query = {
    "q": {
        "field1": "cat"
    }
}

# Execute update with bulk_update
client.bulk_update(update_dict, update_query)
```

Returns a Response dict-like object in the form of
```
{
    'errors': [<items>],
    'success': [<items>]
}
```

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

# Thread safety
The same instance of the client can be shared amongst multiple threads if not using requests, or if using requests with http_keep_alive=False set.

# Error handling

An instance of `sispy.Error` is raised if an HTTP request returns a status code above and including 400.

`sispy.Error` has the following attributes that can be inspected:

* error: SIS error text
* code : SIS error code
* http_status_code : HTTP status code
* response_dict : dictionary representing response body json

Handling connection errors is outside of the client's scope.

# LICENSE

This software is licensed under the BSD 3-Clause license.  Please refer to the [LICENSE](LICENSE) for more information.

