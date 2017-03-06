import sys
import socket
import json
from urlparse import urlparse
from flask import Flask,render_template,request
import twilio.twiml
import logging

#sys.path.append("./helpers" )

app = Flask (__name__)
logging.basicConfig( level=logging.INFO)

@app.route("/welcome/sms/reply/", methods = ['GET','POST'])
def welcomereply():
    resp = twilio.twiml.Response()
    resp.message("I got your message, but i'm not programmed to know how to handle it.")
    logging.info(request.form)
    logging.info(request.values)
    return str(resp)

@app.route("/sayhi/", methods = ['GET','POST'])
def sayhi():
    resp = twilio.twiml.Response()
    resp.message("Hello World")
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
