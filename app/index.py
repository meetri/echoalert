import os
import sys
import socket
import json
from urlparse import urlparse
from flask import Flask,render_template,request
import twilio.twiml
import logging

sys.path.append("./models" )

from pgdb import PgDb
from accounts import Account

app = Flask (__name__)
logging.basicConfig( level=logging.INFO)

@app.route("/welcome/sms/reply/", methods = ['GET','POST'])
def welcomereply():
    resp = twilio.twiml.Response()

    logging.basicConfig( level=logging.INFO)
    connInfo = {
            "dbname": os.getenv('DBNAME', "echoalert"),
            "user": os.getenv('DBUSER', "postgres"),
            "host": os.getenv('DBHOST', "localhost"),
            "port": os.getenv('DBPORT', "5432"),
            "password": os.getenv('DBPASS', "defaultpassword"),
            }

    logging.info("initialized")
    PgDb.setup( **connInfo)

    fr = request.form.get("From")
    sid = request.form.get("SmsMessageSid")
    accountsid = request.form.get("AccountSid")
    smssid = request.form.get("SmsSid")
    body = request.form.get("Body")

    if len(fr) > 0:
        account = Account.get_account_by_phone(fr)
        logging.info("found {} accounts".format(len(account)))

    logging.info("From: {}, Body: {}".format(fr,body))

    resp.message("I got your message, but i'm not programmed to know how to handle it.")
    logging.info(request.form)
    return str(resp)

@app.route("/sayhi/", methods = ['GET','POST'])
def sayhi():
    resp = twilio.twiml.Response()
    resp.message("Hello World")
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
