import json
import time

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from src.helpers import DEBUG

import jwt
JWT_EXP_SECS = 15 * 60  # 15 mins


class UserController:
    def create_user(self, login, password):
        ttl = 16 * 60
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('APIUsersTable')
        user = table.query(KeyConditionExpression=Key("login").eq(login))
        if user["Items"]:
            return "False"
        else:
            user = {
                "login": login,
                "password": password,
                "ttl": ttl
            }
            response = table.put_item(Item=user)
            DEBUG(f"response: {response}")
            token = self.get_token(login=login)
            return token

    def authorization(self, login, password):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('APIUsersTable')
        resp = table.query(KeyConditionExpression=Key("login").eq(login))
        items = resp.get("Items", [])
        if items:
            user = items[0]
            if user["password"] == password:
                token = self.get_token(login)
                return token
        return "User does not exist"

    def get_secret_keys(self):
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
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)

    def get_token(self, login):
        keys = self.get_secret_keys()
        payload = {
            "sub": login,
            "iat": int(time.time()),
            "exp": int(time.time() + JWT_EXP_SECS)
        }
        token = jwt.encode(payload=payload, key=keys.get("private_key"), algorithm="RS256")
        return token
