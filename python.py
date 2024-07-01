import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# The character encoding for the email.
CHARSET = "UTF-8"
# Create a new SES resource and specify a region.
ses_client = boto3.client("ses", region_name="us-east-1")
source_email = "izaanit.dev@gmail.com"

admin_email = "izaanit.sm@gmail.com"

#Dynamodb DB Table 
dynamodb_database = boto3.resource('dynamodb', region_name='us-east-1')
database_table = dynamodb_database.Table('portfolio-table')

def lambda_handler(event, context):
       
        logger.info(event) 
        
        contact_email = event['email']
        contactName = event['contactName'] 
        subject = event['subject'] 
        contactMessage = event['contactMessage'] 
       
        try:

            response = database_table.put_item(
                Item=event
            )
            
            # send Confirmation Email to Recipant
            confirmation_subject = "Thank You for Getting in Touch!"
            confirmation_body = ("Hello," + contactName + " \r\n"
            "We have received your Message.\r\n"
            "Thank you for your Contact!"
            )
            send_mail(contact_email, confirmation_subject, confirmation_body)

            # send Email to Admin
            send_mail(admin_email, subject, contactMessage)

            # send Email to Admin
            return {"statusCode": 200, "IsSuccess": "YES","message": "Saved Successfully!","body": ""}
        except Exception as ex :
            return {"statusCode": 400, "IsSuccess": "No","message": "Please try Again!","body":  "" }
    
def send_mail(RECIPIENT, SUBJECT, BODY_TEXT):
    try:
        # Provide the contents of the email.
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=source_email,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        return { 'statusCode': 400,  'body': e.response['Error']['Message'] }
    else:
        return { 'statusCode': 200, 'body': "Email sent! Message ID: {}".format(response['MessageId']) }