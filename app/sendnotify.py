#!/usr/bin/python -u
import os
import time
import sys
import datetime
import logging

script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_path + "/models")

from pgdb import PgDb
from accounts import Account
from echosite import Echosite
from notify import Notifier
from sms import SmsEngine

logging.basicConfig( level=logging.INFO)


connInfo = {
        "dbname": os.getenv('DBNAME', "echoalert"),
        "user": os.getenv('DBUSER', "postgres"),
        "host": os.getenv('DBHOST', "localhost"),
        "port": os.getenv('DBPORT', "5432"),
        "password": os.getenv('DBPASS', "defaultpassword"),
        }

PgDb.setup( **connInfo)
notifications = Notifier.get_new_notices()

sid = os.getenv("TWILIO_SID","")
token  = os.getenv("TWILIO_TOKEN","")
sms_from  = os.getenv("TWILIO_FROM","")

logging.info("Checking for any pending notifications")
logging.info("twilio sid={}, token={}".format(sid,token))

sms = SmsEngine(sid,token,sms_from)

for ndata in notifications:

    notify_type = ndata['notification_type']
    if notify_type == 1: #grade update
        sms.send("EchoAlert: Grades has been updated",ndata['notification_sms'])
    elif notify_type == 2: #assignment update
        sms.send("EchoAlert: Todo has been updated",ndata['notification_sms'])
    elif notify_type == 3:
        sms.send("EchoAlert: Course has been updated",ndata['notification_sms'])
    elif notify_type == 4:
        sms.send("EchoAlert: Agenda has been updated",ndata['notification_sms'])
    elif notify_type == 5:
        sms.send("EchoAlert: Asset has been updated",ndata['notification_sms'])

    Notifier.mark_sent( ndata['id'],"Message sent successfully" )


