'''sms message'''

from twilio.rest import TwilioRestClient

class SmsEngine(object):

    def __init__(self,sid,token,sms_from):
        self.sms_from = sms_from
        self.client = TwilioRestClient(account=sid,token=token)

    def send( self,msg, number):
        message = self.client.messages.create(to=number, from_= self.sms_from ,
                                                     body=msg)

