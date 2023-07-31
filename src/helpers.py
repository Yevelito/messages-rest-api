import datetime
import decimal
import json
import os

import boto3
import jwt
from botocore.exceptions import ClientError
from jwt import InvalidSignatureError, ExpiredSignatureError


def DEBUG(*args, **kwargs):
    log_level = os.environ.get("LOG_LEVEL")
    if log_level == "1":
        print("DEBUG({}): {}".format(datetime.datetime.now(), *args, **kwargs))


def ERROR(*args, **kwargs):
    log_level = os.environ.get("LOG_LEVEL")
    if log_level == "1" or log_level == "2":
        print("ERROR({}): {}".format(datetime.datetime.now(), *args, **kwargs))


def get_secret():
    secret_name = "jwt_keys"
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    keys = json.loads(get_secret_value_response['SecretString'])

    private_key = keys.get("JWT_PRIVATE_KEY").replace(" ", "\n")
    private_key = f"-----BEGIN RSA PRIVATE KEY-----\n{private_key}\n-----END RSA PRIVATE KEY-----"
    public_key = keys.get("JWT_PUBLIC_KEY").replace(" ", "\n")
    public_key = f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"

    return {"public_key": public_key, "private_key": private_key}


def validate(token: str) -> bool:
    DEBUG(f"Validating token: {token}")
    if not token:
        return False
    token_auth_type = token.split(" ")[0]
    token_auth_value = token.split(" ")[1]
    DEBUG(token_auth_type)
    DEBUG(token_auth_value)
    keys = get_secret()
    try:
        decoded = jwt.decode(token_auth_value, key=keys.get("public_key"), algorithms=["RS256"])
    except InvalidSignatureError as e:
        print("Invalid token")
        print(e)
        return False
    except ExpiredSignatureError as e:
        print("Token expired")
        print(e)
        return False
    return True


class SuccessRequest:
    @staticmethod
    def http(body, default=None) -> dict:
        body = json.dumps(body, separators=(',', ':'), default=default, cls=DecimalEncoder)
        return {
            "statusCode": 200,
            "body": body,
            "headers": {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true',
                'Content-type': 'application/json'
            }
        }


class Unauthorized(Exception):
    @staticmethod
    def http(
            code: int = 401,
            message="401 Unauthorized",
            default=None) -> dict:
        body = json.dumps({"message": message}, default=default, cls=DecimalEncoder)
        return {
            "statusCode": code,
            "body": body,
            "headers": {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true'
            }
        }


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self).default(o)
