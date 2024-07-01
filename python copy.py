import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)



def lambda_handler(event, context):
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        logger.info(event)
        #json_data = json.loads(event)
        table = dynamodb.Table('portfolio-table')
        email = event['email']
        
        try:

            _response = table.put_item(
                Item=event
            )
            return {"statusCode": 200, "IsSuccess": "YES","message": "Saved Successfully!","body": json.dumps({ 'Message':"",'response':""})}
        except Exception as ex :
            return {"statusCode": 400, "IsSuccess": "No","message": "Please try Again!","body": json.dumps({ 'Message':"Error in DB",'response':""}) }





