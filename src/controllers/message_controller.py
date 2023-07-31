import time
import uuid
import boto3
from boto3.dynamodb.conditions import Key

from src.helpers import DEBUG

MSG_EXP_SECS = 15 * 60  # 15 mins

class MessageController:

    def save_message_to_db(self, text) -> str:
        msg_id = uuid.uuid4().__str__()
        current_time = int(time.time())
        message = {
            "id": msg_id,
            "time": current_time,
            "text": text,
            "ttl": int(time.time() + MSG_EXP_SECS)
        }
        DEBUG("MESSAGE TO DB: {}".format(message))

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('APIMessagesTable')
        response = table.put_item(Item=message)
        DEBUG(f"response: {response}")
        return msg_id

    def get_message_from_db_by_id(self, message_id):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('APIMessagesTable')
        response = table.query(KeyConditionExpression=Key("id").eq(message_id))
        return response.get('Items', [])

    def get_messages_from_db(self):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('APIMessagesTable')
        response = table.scan()
        return response.get('Items', [])

    def delete_message_from_db_by_id(self, message_id):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('APIMessagesTable')

        response = table.delete_item(
            Key={
                'id': message_id
            }
        )
        DEBUG(response)
        return "Success"

    def delete_messages_from_db(self):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('APIMessagesTable')
        items = table.scan().get("Items", [])

        for item in items:
            resp = table.delete_item(Key={'id': item['id']})
            DEBUG(resp)

        return "Success"
