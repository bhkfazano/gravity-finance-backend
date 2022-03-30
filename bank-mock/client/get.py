from libs.response import notfound, success, failure
from boto3.dynamodb.conditions import Attr
import boto3
import os

def get(event, context):
    """
    Receives a cpf and returns the client
    """
    print(event)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_CLIENT_TABLE'])

    try:
        client = table.get_item(Key={'cpf': event['pathParameters']['cpf']})
    except Exception as e:
        print(e)
        return failure({"Error getting client data" : e})

    if 'Item' not in client:
        return notfound("No client found for the specified cpf")
    
    return success(client['Item'])
