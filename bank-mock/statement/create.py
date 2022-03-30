from libs.response import failure, success, missingData
from libs.auth import decode_jwt
from decimal import Decimal
import datetime
import boto3
import uuid
import json
import os


def create(event, body):
    """
    Creates a entry on the statements' dynamodb table
    Body format: {
        "name": "string",
        "cpf": "string",
        "value": "string"
        "currency": "string"
        "type": "string",
    }
    """
    print(event)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_STATEMENT_TABLE'])

    # Retrieves the request body and validates it
    body = json.loads(event['body'])
    token = event['headers']['Authorization'].split(' ')[1]

    cpf = validate_token(token)
    if not cpf:
        return failure({"Error": "Invalid token"})

    # Put item into dynamodb table
    item = {
        "statement_id": str(uuid.uuid4()),
        "name": body['name'],
        "cpf": cpf,
        "value": body['value'],
        "currency": body['currency'],
        "type": body['type'],
        "created_at" : datetime.datetime.now().isoformat(),
    }
    
    try:
        table.put_item(Item=json.loads(json.dumps(item), parse_float=Decimal))
        return success(item)
    except Exception as e:
        print(e)
        return failure({"Error while creating entry" : e})


def validate_token(token):

    # Decode the token
    try:
        decoded_token = decode_jwt(token)
        return decoded_token['cpf']
    except Exception as e:
        print(e)
        return False

