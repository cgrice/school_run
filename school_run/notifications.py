import os
import json
import boto3

def send_sms(message):
    queue_name = os.environ.get('NOTIFICATIONS_QUEUE', 'notifications-outbound')
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=queue_name)

    body = json.dumps({
        "type": "notifications.send",
        "medium": "sms",
        "recipients": ["chris"],
        "message": message,
    })
    response = queue.send_message(MessageBody=body)

