# Install the Python helper library from twilio.com/docs/python/install
import os

from twilio.rest import Client

def send_msg(message):
    ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
    AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
    NOTIFICATION_SERVICE = os.environ.get('NOTIFICATION_SERVICE')

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    notification = client.notify.services(NOTIFICATION_SERVICE) \
        .notifications.create(
            to_binding='{"binding_type":"sms", "address":"' + os.environ.get('NUMBER1') + '"}',
            body=message)
