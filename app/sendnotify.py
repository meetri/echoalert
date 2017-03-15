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
from grades import GradeSummary
from assignments import Assignment

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

skip = []
for ndata in notifications:

    notify_type = ndata['notification_type']
    if notify_type not in skip:
        skip += [ notify_type ]

        if notify_type == 1: #grade update
            res = GradeSummary.compare_grades_after( ndata['account_id'],ndata['created_ts'])
            for idx in xrange(0,len(res),2):
                if idx+1 < len(res):
                    a = "up"
                    s = res[idx].get("score")
                    d = res[idx].get("score") - res[idx+1].get("score")
                    if d < 0:
                        a = "down"

                    msg = "grade in {} is {}, it has gone {} by {}%".format(res[idx].get("course_name"),s,a,abs(d))
                    sms.send(msg,ndata['notification_sms'])

        elif notify_type == 2: #assignment update
            sms.send("EchoAlert: Todo has been updated",ndata['notification_sms'])
        elif notify_type == 3:
            sms.send("EchoAlert: Course has been updated",ndata['notification_sms'])
        elif notify_type == 4:
            res = Assignment.get_assignments_after( ndata['account_id'],ndata['created_ts'])
            for idx in xrange(0,len(res)):
                title = res[idx].get("title")
                if len(title) > 64:
                    title = title[0:64].strip()
                if "Past Due" in res[idx].get("due"):
                    msg = """{}:\n{}\n{}...""".format( res[idx].get("course_name"),res[idx].get("due"),title)
                    sms.send(msg,ndata['notification_sms'])
                else:
                    msg = """{}:\nDue: {}\n{}...""".format( res[idx].get("course_name"),res[idx].get("due"), title)
                    sms.send(msg,ndata['notification_sms'])

        elif notify_type == 5:
            sms.send("EchoAlert: Asset has been updated",ndata['notification_sms'])

    Notifier.mark_sent( ndata['id'],"Message sent successfully" )


