import json
import time

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from src.helpers import DEBUG, get_secret

import jwt
JWT_EXP_SECS = 15 * 60  # 15 mins
USER_EXP_SECS = 60 * 60  # 60 mins


class UserController:
    def create_user(self, login, password):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('APIUsersTable')
        user = table.query(KeyConditionExpression=Key("login").eq(login))
        if user["Items"]:
            return "False"
        else:
            user = {
                "login": login,
                "password": password,
                "ttl": int(time.time() + USER_EXP_SECS)
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


    def get_token(self, login):
        keys = get_secret()
        payload = {
            "sub": login,
            "iat": int(time.time()),
            "exp": int(time.time() + JWT_EXP_SECS)
        }
        token = jwt.encode(payload=payload, key=keys.get("private_key"), algorithm="RS256")
        return token
