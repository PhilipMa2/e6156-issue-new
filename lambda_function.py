import json
import boto3
import os
from datetime import datetime

client = boto3.client('ses', region_name='us-east-2')

def lambda_handler(event, context):
    if os.environ.get('IS_ENABLED') != 'true':
        print("SES is disabled. Exiting without sending email.")
        return
    
    response = client.send_email(
       Destination={
           'ToAddresses': ['lz2933@columbia.edu']
       },
       Message={
           'Body': {
               'Text': {
                   'Charset': 'UTF-8',
                   'Data': 'There is a new user report issue.',
               }
           },
           'Subject': {
               'Charset': 'UTF-8',
               'Data': 'New Issue',
           },
       },
       Source='oliviaz0826@outlook.com'
    )
    
    print("check")
    print(response)
    
    return {
        'statusCode': 200,
        'body': json.dumps("Email Sent Successfully. MessageId is: " + response['MessageId'])
    }