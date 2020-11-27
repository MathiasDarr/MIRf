"""
This script creates the dynamoDB transcriptions table

"""
# !/usr/bin/env python3

import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-west-2') #, endpoint_url='http://localhost:8000')
try:
    resp = dynamodb.create_table(
        AttributeDefinitions=[
            {
                "AttributeName": "user",
                "AttributeType": "S"
            },
            {
                "AttributeName": "filename",
                "AttributeType": "S"
            },
        ],
        TableName="UserUploads",
        KeySchema=[
            {
                "AttributeName": "user",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "filename",
                "KeyType": "RANGE"
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1
        },
    )

except Exception as e:
    print(e)

