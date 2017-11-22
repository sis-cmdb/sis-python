# -*- coding: utf-8 -*-

import unittest
import random
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

        # Update_bulk (List) run the test 25 times
        for m in range(25):
            # Store all entities into a variable
            resp = self.client.entities(self.test_schema_name).fetch_all().to_list()
            # Initialize content list to pass into bulk_update method
            content = []

            # Temporary numList to choose 5 random entities to update adds 5 random numbers to numList
            numList = []
            for i in range (5):
                randNum = random.randint(0, 999)
                # Check to make sure no duplicate entries are added
                if randNum not in numList:
                    numList.append(randNum)
                else:
                    while randNum in numList:
                        randNum = random.randint(0, 999)
                    numList.append(randNum)

            # Add dictionary of values to the content list field1 and field2 store the random number generated
            for x in numList:
                content.append(
                    {
                        "_id": resp[x]['_id'],
                        "field1": x,
                        "field2": str(x)
                    }
                )
                print("Updating " + resp[x]['_id'] + " To: " + str(x))
            # Call bulk update method on the 5 entities chosen at random
            response = self.client.entities(self.test_schema_name).update_bulk(content)
            
            # Assert Statement to see if there are 5 successful updates
            self.assertEqual(len(response['success']), 5)

            # Loop to check if the values have changed and are equal
            for item in content:
                temp_id = item["_id"]

                # Loop through content list, grab the id and check field1 of that id
                field1 = self.client.entities(self.test_schema_name).get(temp_id)['field1']

                # field1 in sis should be equal to field1 from content list
                self.assertEqual(field1, item['field1'])



        # Update Bulk (Query) run the test 25 times
        for n in range(25):
            # numList2 used to choose 4 random entities
            numList2 = []
            # Store the entities into a variable temporarily
            resp2 = self.client.entities(self.test_schema_name).fetch_all().to_list()

            # Add random numbers to numList2
            for i in range(4):
                randNum = random.randint(0, 999)
                # Check to make sure no duplicate entries are added
                if randNum not in numList2:
                    numList2.append(randNum)
                else:
                    while randNum in numList2:
                        randNum = random.randint(0, 999)
                    numList2.append(randNum)

            # Loops through random entities chosen in numList2 and updates field2 to cat
            for x in numList2:
                temp_id2 = resp2[x]["_id"]
                print("Updating " + resp[x]['_id'] + " To: dog")
                self.client.entities(self.test_schema_name).update(temp_id2, {"field2": "cat"})
            
            # Bulk Update call with query. Will update the entities that have cat as field2
            # Changes the value of field2 from cat to dog
            response = self.client.entities(self.test_schema_name).update_bulk({"field2": "dog"}, query = {
                    'q': {"field2": {"$eq": "cat"}}
                })

            # Loop through the chosen entities and checks to see if field2 is equal to dog
            for x in numList2:
                temp_id2 = resp2[x]["_id"]
                field2 = self.client.entities(self.test_schema_name).get(temp_id2)['field2']

                # Field2 should now be dog instead of cat
                self.assertEqual(field2, "dog")

            # There should be 4 successful updates
            self.assertEqual(len(response['success']), 4)

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

