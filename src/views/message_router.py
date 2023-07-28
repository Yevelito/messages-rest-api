import json
import uuid

from src.controllers.message_controller import MessageController

import boto3
from aws_lambda_powertools.event_handler.api_gateway import Router

from src.helpers import DEBUG

router = Router()


@router.post("/")
def test():
    random_id = uuid.uuid4().__str__()
    return random_id


@router.post("/messages")
def post_message():
    event = router.current_event
    DEBUG(f"POST REQUEST: {event}")

    body = json.loads(event.body)
    DEBUG(f"BODY OF POST REQUEST: {body}")

    controller = MessageController()
    result = controller.save_message_to_db(body)
    return result


@router.get("/messages")
def get_messages():
    controller = MessageController()
    result = controller.get_messages_from_db()
    return result


@router.get("/messages/<message_id>")
def get_message_by_id(message_id):
    controller = MessageController()
    result = controller.get_message_from_db_by_id(message_id=message_id)
    return result


@router.delete("/messages")
def delete_messages():
    controller = MessageController()
    result = controller.delete_messages_from_db()
    return result


@router.delete("/messages/<message_id>")
def delete_message_by_id(message_id):
    controller = MessageController()
    result = controller.delete_message_from_db_by_id(message_id=message_id)
    return result
