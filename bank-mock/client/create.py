from libs.response import failure, success, missingData
from libs.auth import create_jwt
from decimal import Decimal
import datetime
import boto3
import uuid
import json
import os


def create(event, body):
    """
    Creates a entry on the clients' dynamodb table
    Body format: {
        "cpf": "string",
        "password": "string"
    }
    """

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_CLIENT_TABLE'])

    # Retrieves the request body and validates it
    body = json.loads(event['body'])

    # Put item into dynamodb table
    item = {
        "cpf": body['cpf'],
        "password": create_jwt({'password' : body['password']}),
        "created_at" : datetime.datetime.now().isoformat(),
        "updated_at" : datetime.datetime.now().isoformat()
    }
    
    try:
        table.put_item(Item=json.loads(json.dumps(item), parse_float=Decimal))
        return success(item)
    except Exception as e:
        print(e)
        return failure({"Error while creating client" : e})