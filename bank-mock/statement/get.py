from libs.response import notfound, success, failure
from libs.auth import decode_jwt
from boto3.dynamodb.conditions import Attr
import boto3
import os

def get(event, context):
    """
    Receives a cpf and returns the statement for the given cpf
    """
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_STATEMENT_TABLE'])
    token = event['headers']['Authorization'].split(' ')[1]

    cpf = validate_token(token)
    if not cpf:
        return failure({"Error": "Invalid token"})

    entries = False

    try:
        entries = table.scan(FilterExpression=Attr('cpf').eq(cpf))
    except Exception as e:
        print(e)
        return failure({"Error getting job data" : e})

    if 'Items' not in entries or len(entries['Items']) == 0:
        return notfound("No entries found for the specified cpf")

    return success(entries['Items'])


def validate_token(token):

    # Decode the token
    try:
        decoded_token = decode_jwt(token)
        return decoded_token['cpf']
    except Exception as e:
        print(e)
        return False
