import jwt

from src.helpers import DEBUG, get_secret


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