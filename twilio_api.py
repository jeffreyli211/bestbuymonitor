import os
from twilio.rest import Client

# class twilio_class:
account_sid = os.environ['TWILIO_SID']
service_sid = os.environ['TWILIO_SERVICE_SID']
auth_token = os.environ['TWILIO_SECRET']
twilio_number = os.environ['TWILIO_NUMBER']
client = Client(account_sid, auth_token) 

# Craft a Twilio SMS message to be sent to designated phone number
def send_sms(url, phone_number):
    message = client.messages.create(  
                                messaging_service_sid=service_sid, 
                                body='An item you are monitoring is in stock on Best Buy! Here is a link:\n' + str(url),      
                                to=phone_number
                            )