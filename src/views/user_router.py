import json
from aws_lambda_powertools.event_handler.api_gateway import Router

from src.controllers.user_controller import UserController
from src.helpers import DEBUG, SuccessRequest

router = Router()


@router.post("/reg")
def singup():
    event = router.current_event
    DEBUG(f"AUTH POST REQUEST: {event}")

    body = json.loads(event.body)
    DEBUG(f"AUTH BODY OF POST REQUEST: {body}")

    controller = UserController()
    result = controller.create_user(body["login"], body["password"])
    # return result
    return SuccessRequest.http(body=result)


@router.post("/auth")
def login():
    event = router.current_event
    DEBUG(f"AUTH GET REQUEST: {event}")

    body = json.loads(event.body)
    DEBUG(f"AUTH BODY OF GET REQUEST: {body}")

    controller = UserController()
    result = controller.authorization(body["login"], body["password"])
    # return result
    return SuccessRequest.http(body=result)
