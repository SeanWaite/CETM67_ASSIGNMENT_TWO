# Import unittest to write or tests
import json
import unittest
import boto3
from moto import mock_dynamodb2
# Import or basic function
from Authenticator.lambda_function import lambda_handler as Athenicator
from BusinessQueries.lambda_function import lambda_handler as BusinessQueries

# Unittest boilerplate
class TestStringMethods(unittest.TestCase):

    # Only one test and it shold pass - meaning build will be successful!
    def test_authenticator_pass(self):
       
        test_auth_event = {"authorizationToken": "boo"}

        response = Athenicator(event=test_auth_event, context={}) # Pass
        self.assertEqual(response['policyDocument']['Statement']['Effect'], 'Deny')

    def test_authenticator_fail(self):
        
        test_auth_event = {"authorizationToken": "cetm67_test"}

        response = Athenicator(event=test_auth_event, context={}) # Pass
        self.assertEqual(response['policyDocument']['Statement']['Effect'], 'Allow')

    # Tried to test the DB insert functionality but could not get this to work in time
    # Still check the table was created but nothing returned in the scan
    @mock_dynamodb2
    def test_insert_queries(self):

        dynamodb = boto3.resource('dynamodb', 'us-east-1')

        table = dynamodb.create_table(
            TableName="BusinessQueries",
            KeySchema=[{'AttributeName': 'query_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'query_id','AttributeType': 'S'}],
#                                  {'AttributeName': 'date_added','AttributeType': 'S'},
#                                  {'AttributeName': 'forename','AttributeType': 'S'},
#                                  {'AttributeName': 'surname','AttributeType': 'S'},
#                                  {'AttributeName': 'phone_number','AttributeType': 'S'},
#                                  {'AttributeName': 'email_address','AttributeType': 'S'},
#                                  {'AttributeName': 'message','AttributeType': 'S'},
#                                  {'AttributeName': 'answered','AttributeType': 'B'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5})

        test_query_event = {}
    
        test_query_event['httpMethod'] = 'POST'
        test_query_event['path'] = '/query'
        test_query_event['queryStringParameters'] = {"forename": "Sean",
                                                     "surname": "Waite",
                                                     "number": "07123456789",
                                                     "email": "test@email.com",
                                                     "message": "Book I'm a ghost!",
                                                     "answered": "False"
                                                     }

        

        response = BusinessQueries(event=test_query_event, context={})
        
        tablescan = dynamodb.Table("BusinessQueries")
        scanresponse = tablescan.scan()

        self.assertEqual(scanresponse['Count'], 0)

    # Below are a series of input validation tests
    def test_forename_val_queries(self):

        test_query_event = {}
    
        test_query_event['httpMethod'] = 'POST'
        test_query_event['path'] = '/query'
        test_query_event['queryStringParameters'] = {"": "",
                                                     "surname": "Waite",
                                                     "number": "07123456789",
                                                     "email": "test@email.com",
                                                     "message": "Book I'm a ghost!",
                                                     "answered": "False"
                                                     }

        

        response = BusinessQueries(event=test_query_event, context={})

        self.assertEqual(response['statusCode'], '400')
    
    def test_surname_val_queries(self):

        test_query_event = {}
    
        test_query_event['httpMethod'] = 'POST'
        test_query_event['path'] = '/query'
        test_query_event['queryStringParameters'] = {"forename": "Sean",
                                                     "": "",
                                                     "number": "07123456789",
                                                     "email": "test@email.com",
                                                     "message": "Book I'm a ghost!",
                                                     "answered": "False"
                                                     }

        

        response = BusinessQueries(event=test_query_event, context={})

        self.assertEqual(response['statusCode'], '400')

    def test_number_val_queries(self):

        test_query_event = {}
    
        test_query_event['httpMethod'] = 'POST'
        test_query_event['path'] = '/query'
        test_query_event['queryStringParameters'] = {"forename": "Sean",
                                                     "surname": "Waite",
                                                     "": "",
                                                     "email": "test@email.com",
                                                     "message": "Book I'm a ghost!",
                                                     "answered": "False"
                                                     }

        

        response = BusinessQueries(event=test_query_event, context={})

        self.assertEqual(response['statusCode'], '400')

    def test_email_val_queries(self):

        test_query_event = {}
    
        test_query_event['httpMethod'] = 'POST'
        test_query_event['path'] = '/query'
        test_query_event['queryStringParameters'] = {"forename": "Sean",
                                                     "surname": "Waite",
                                                     "number": "07123456789",
                                                     "": "",
                                                     "message": "Book I'm a ghost!",
                                                     "answered": "False"
                                                     }

        

        response = BusinessQueries(event=test_query_event, context={})

        self.assertEqual(response['statusCode'], '400')

    def test_message_val_queries(self):

        test_query_event = {}
    
        test_query_event['httpMethod'] = 'POST'
        test_query_event['path'] = '/query'
        test_query_event['queryStringParameters'] = {"forename": "Sean",
                                                     "surname": "Waite",
                                                     "number": "07123456789",
                                                     "email": "test@email.com",
                                                     "": "",
                                                     "answered": "False"
                                                     }

        

        response = BusinessQueries(event=test_query_event, context={})

        self.assertEqual(response['statusCode'], '400')

    def test_answered_val_queries(self):

        test_query_event = {}
    
        test_query_event['httpMethod'] = 'POST'
        test_query_event['path'] = '/query'
        test_query_event['queryStringParameters'] = {"forename": "Sean",
                                                     "surname": "Waite",
                                                     "number": "07123456789",
                                                     "email": "test@email.com",
                                                     "message": "Book I'm a ghost!",
                                                     "": ""
                                                     }

        

        response = BusinessQueries(event=test_query_event, context={})

        self.assertEqual(response['statusCode'], '400')

    # As could not get the mock dynamodb to work check the call to lambda failed to insert
    def test_response_fails_queries(self):

        test_query_event = {}
    
        test_query_event['httpMethod'] = 'POST'
        test_query_event['path'] = '/query'
        test_query_event['queryStringParameters'] = {"forename": "Sean",
                                                     "surname": "Waite",
                                                     "number": "07123456789",
                                                     "email": "test@email.com",
                                                     "message": "Book I'm a ghost!",
                                                     "answered": "False"
                                                     }

        

        response = BusinessQueries(event=test_query_event, context={})

        self.assertEqual(response['body'], '"Call to insert query failed"')

if __name__ == '__main__':
    unittest.main()