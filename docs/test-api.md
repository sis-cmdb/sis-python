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
t = Test(url='https://sis.myorg.com',
         username=username,
         password=password,
         owner='ops')

# run tests
unittest.TextTestRunner().run(t)
```

