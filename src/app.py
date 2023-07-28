import jwt
from aws_lambda_powertools.event_handler import APIGatewayRestResolver

from src.helpers import DEBUG, ERROR, get_secret
from src.views import message_router, user_router

app = APIGatewayRestResolver(strip_prefixes=['/test'])
app.include_router(message_router.router)
app.include_router(user_router.router)


def handler(event, context):
    DEBUG(event)
    return app.resolve(event, context)


def auth(event, context):
    DEBUG(event)
    DEBUG(event.get("authorizationToken"))
    token = event.get("authorizationToken")

    keys = get_secret()
    payload = jwt.decode(token, key=keys.get("public_key"), algorithms=["RS256"])
    policy = {
        'principalId': payload["sub"],
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "Allow",
                    "Resource": "*"

                }
            ]
        }
    }
    return policy
