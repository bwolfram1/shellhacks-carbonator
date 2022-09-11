import os
import pymongo
import json
import time
from twilio.rest import Client

def dummy(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    if request.method == 'OPTIONS':
        # Allows GET requests from origin https://mydomain.com with
        # Authorization header
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Credentials': 'true'
        }
        return ('', 204, headers)

    # Set CORS headers for main requests
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': 'true'
    }

    request_json = request.get_json()
   
    account_sid = os.environ.get('twiliosid')
    auth_token  = os.environ.get('twiliotoken')
    sender  = os.environ.get('sender')
    client = Client(account_sid, auth_token)
    
    if request_json:
        # payload["sender"] = request_json['sender']
        receiver = request_json['receiver']
        text = request_json['message']        
        retjson = {}
 
        if request_json['token'] == "SHELLHACKS2022-CARBONATOR":


            message = client.messages.create( 
                                from_=sender,  
                                body=text,      
                                to=receiver 
                            )

            result=message.sid
            retjson['result'] = 'sent successfully'
        else:
            retjson['result'] = 'invalid token'


        # retjson['sid'] = result
        # retjson['result'] = "successfully sent"

        return json.dumps(retjson)


    retstr = "action not done"

    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return retstr
