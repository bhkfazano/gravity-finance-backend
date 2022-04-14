import json
from libs.response import failure, success, missingData
from libs.auth import create_jwt, decode_jwt
import boto3
import os

def authenticate(event, context):
    """
    Receives an access code and a cpf and password and returns a jwt
    """
    
    body = json.loads(event['body'])

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_CLIENT_TABLE'])
    client = False

    try:
        client = table.get_item(Key={'cpf': body['cpf']})
    except Exception as e:
        print(e)
        return failure({"Error getting client data": e})

    if client:
        if decode_jwt(client['Item']['access_code'])['access_code'] == body['access_code']:
            return success(create_jwt({'cpf':client['Item']['cpf']}))
        else:
            return failure({"Error": "Invalid code"})


