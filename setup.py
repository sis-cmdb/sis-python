# -*- coding: utf-8 -*-
from distutils.core import setup

import sispy

version = '.'.join([ str(sispy.__version__[i]) for i in range(3) ])

setup (
    name='sispy',
    version=version,
    author=sispy.__author__,
    description='Python client library for interacting with the SIS RESTful API',
    packages=['sispy'],
    url='https://github.com/sis-cmdb/sis-python',
    download_url='https://github.com/sis-cmdb/sis-python/tarball/v%s' % version,
    license='BSD 3-Clause'
)

