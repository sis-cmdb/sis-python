# -*- coding: utf-8 -*-

from distutils.core import setup

import sispy

try:
    import httplib2
except ImportError:
    print(
        "\n"
        "\033[1m"
        "Attention! You don't seem to have httplib2 installed, "
        "please consider installing it to improve the client's performance"
        "\033[0m"
        "\n"    
    )

version = '.'.join([ str(sispy.__version__[i]) for i in range(3) ])

setup (
    name='sispy',
    version=version,
    author=sispy.__author__,
    description='Python client library for interacting with the SIS RESTful API',
    packages=['sispy'],
    url='https://github.com/sis-cmdb/sis-python',
    download_url='https://github.com/sis-cmdb/sis-python/tarball/%s' % version
)

