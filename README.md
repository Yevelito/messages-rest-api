# Messages-rest-api
Simple REST API project based on AWS with Serverless framework.

Included capabilities: 
- registration user with 1 hour TTL
- authorization with JWT token
- posting messages with 15 minutes TTL
- getting messages
- deleting messages

Consist of 4 types of routes:

    /reg
    /auth
    /messages
    /messages/<message_id>

## Requests:

___

### POST registration
    POST /reg

Registration user for 1 hour. 

Body should be in **JSON** format.

Body example: 

    {
       login: "your login",
       password: "your password"
    }

___

### POST authorization
    POST /auth

Authorization.
Body should be in **JSON** format.

Body example: 

    {
       login: "your login",
       password: "your password"
    }

### Response
Bearer Token in text format.

This TOKEN you put to authorization header to get an access POST/GET/DELETE requests on **/messages** url. 

___

### POST messages
    POST /messages
Post 1 message to dynamoDB. It will be valid for next 15 minutes.
Body should be in **text** format. 

### Response
Message ID in text format.

___

### GET messages
    GET /messages
Get all messages from dynamoDB.

### Response
List of all available messages from all users.

### GET message by ID
    GET /messages/<message_id>
Get specific message by message's ID.

### Response
A message.

___

### DELETE messages
    DELETE /messages 

Delete all messages from dynamoDB for all users.

### Response
Status.

___

### Request
    DELETE /messages/<message_id>
Delete specific message from dynamoDB by message's ID.

### Response
Status.

___

API running domain:
https://08dlfd9x5d.execute-api.us-east-1.amazonaws.com/dev
