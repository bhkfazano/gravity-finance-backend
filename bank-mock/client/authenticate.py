import json
from libs.response import failure, success, missingData
from libs.auth import create_jwt, decode_jwt
import boto3
import os

def authenticate(event, context):
    """
    Receives cpf and password and returns a jwt
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
        print(client)
        if decode_jwt(client['Item']['password'])['password'] == body['password']:
            return success(create_jwt({'cpf':client['Item']['cpf']}))
        else:
            return failure({"Error": "Invalid password"})


