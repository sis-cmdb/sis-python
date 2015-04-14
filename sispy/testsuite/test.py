# -*- coding: utf-8 -*-

import unittest

from sispy import Client, Error

class Test(unittest.TestCase):

    def __init__(
        self, url, username, password, owner, 
        test_schema_name='python_client_test',
    ):
        super(Test, self).__init__()

        self.url = url
        self.username = username
        self.password = password
        self.owner = owner
        self.test_schema_name = test_schema_name    

    def setUp(self):
        self.client = Client(url=self.url)

        # auth
        self.client.authenticate(self.username, self.password)
        self.assertIsNotNone(self.client.auth_token)

    def tearDown(self):
        response = self.client.schemas.delete(self.test_schema_name)

    def runTest(self):
        # create schema
        content = {
            'name': self.test_schema_name,
            'track_history': False,

            '_sis': {
                'owner': self.owner,
            },

            'definition': {
                'field1': 'Number',
            }
        }
        response = self.client.schemas.create(content)

        # create entities
        num = 1000
        for i in range(num):
            content = {
                'field1':  i,
            }
            response = self.client.entities(
                self.test_schema_name).create(content)

        # search for entitites
        response = self.client.entities(self.test_schema_name).fetch_all()

        self.assertIsInstance(response._result, list)
        self.assertEqual(len(response), num)

        # update schema
        content = {
            'name': self.test_schema_name,

            '_sis': {
                'owner': self.owner,
            },

            'definition': {
                'field1': 'Number',
                'field2': 'String',
            }
        }

        response =  self.client.schemas.update(self.test_schema_name, content) 
        self.assertTrue('field2' in response['definition']) 

        # delete_bulk
        response =  self.client.entities(self.test_schema_name).delete_bulk(
            query = {
                'q': { 'field1': 1 }
            }
        )
        self.assertEqual(len(response['success']), 1)

        # error
        self.assertRaises(
            Error,
            self.client.entities(
                'made-up-non-existent-stuff-FAsfsd324'
            ).fetch_all,
        )

