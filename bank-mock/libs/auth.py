import jwt
import os

def create_jwt(payload):
    """
    Creates a jwt token with the payload
    """
    return jwt.encode(payload, os.environ['JWT_SECRET'], algorithm='HS256')

def decode_jwt(token):
    """
    Decodes the jwt token
    """
    try:
        decoded = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    except Exception as e:
        return False