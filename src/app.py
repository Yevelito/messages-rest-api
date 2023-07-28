from aws_lambda_powertools.event_handler import APIGatewayRestResolver


from src.helpers import DEBUG, ERROR, get_secret
from src.views import message_router, user_router

app = APIGatewayRestResolver(strip_prefixes=['/test'])
app.include_router(message_router.router)
app.include_router(user_router.router)


def handler(event, context):
    DEBUG(event)
    return app.resolve(event, context)


