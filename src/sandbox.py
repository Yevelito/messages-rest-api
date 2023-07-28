import json
import time

import boto3
from botocore.exceptions import ClientError
from jwt import InvalidSignatureError

from src.controllers.message_controller import MessageController
from src.controllers.user_controller import UserController
import jwt

JWT_EXP_SECS = 15 * 60  # 15 mins


def get_secret():
    secret_name = "jwt_keys"
    region_name = "us-east-1"

    # Create a Secrets Manager client
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

    keys = json.loads(secret)

    private_key = keys.get("JWT_PRIVATE_KEY").replace(" ", "\n")
    private_key = f"-----BEGIN RSA PRIVATE KEY-----\n{private_key}\n-----END RSA PRIVATE KEY-----"
    public_key = keys.get("JWT_PUBLIC_KEY").replace(" ", "\n")
    public_key = f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"

    return {"public_key": public_key, "private_key": private_key}


if __name__ == '__main__':
    login = "Y"
    password = "123"

    keys = get_secret()

    payload = {
        "sub": login,
        "iat": int(time.time()),
        "exp": int(time.time() + JWT_EXP_SECS)
    }
    token = jwt.encode(payload=payload, key=keys.get("private_key"), algorithm="RS256")
    print(token)

    try:
        decoded = jwt.decode(token, key=keys.get("public_key"), algorithms=["RS256"])
        print(decoded)
    except InvalidSignatureError as e:
        print("Invalid token")
        print(e)
