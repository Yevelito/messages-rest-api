import time

import jwt
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from jwt import InvalidSignatureError

from src.helpers import DEBUG, ERROR, get_secret
from src.views import message_router, user_router

app = APIGatewayRestResolver(strip_prefixes=['/test'])
app.include_router(message_router.router)
app.include_router(user_router.router)


def handler(event, context):
    DEBUG(event)
    auth = validate(event.get("headers", {}).get("Authorization"))
    if not auth:
        return "Unauthorized.Sorry"
    return app.resolve(event, context)


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
    exp_date = decoded.get("exp")
    if exp_date < time.time():
        return False
    return True
