'''sms message'''

import logging
from twilio.rest import TwilioRestClient

class SmsEngine(object):

    def __init__(self,sid,token,sms_from):
        self.sms_from = sms_from
        self.client = TwilioRestClient(account=sid,token=token)

    def send( self,msg, number):
        logging.info(msg)
        number = "+14158859518"
        numlist = number.split(",")
        for num in numlist:
            num = num.strip()
            message = self.client.messages.create(to=num, from_= self.sms_from , body=msg)

