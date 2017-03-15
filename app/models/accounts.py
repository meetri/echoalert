'''access echo grade detils'''

import sys
import time
import logging
import psycopg2
import psycopg2.extras
from pgdb import PgDb
from courses import Course
from notify import Notifier
from datetime import datetime


class Account(object):

    def __init__(self,data):
        self.data = data
        self.courses = None
        # make sure notification date is before and updated events
        self.notify_date = datetime.now()

    def notify(self, notifyType ):
        Notifier.insert( self.data['id'], notifyType, self.notify_date )


    def add_courses(self, courses ):
        self.courses = Course.add_courses( self.data['id'],courses )

    def get_courses(self):
        if self.courses == None:
            self.courses = Course.get_courses( self.data['id'] )

        return self.courses


    @staticmethod
    def get_user_paginate ( start,limit ):
        cur = PgDb.getInstance().get_dict_cursor()
        cur.execute("SELECT id,echo_username,echo_password, notification_email,notification_sms,echo_site FROM echoalert.accounts ORDER BY id asc offset %s limit %s",(start,limit))
        res = cur.fetchall()
        cur.close()

        userlist = []
        for user in res:
            userlist += [ Account(user) ]

        return userlist


    @staticmethod
    def get_user_by_username ( uname ):
        cur = PgDb.getInstance().get_dict_cursor()
        cur.execute("SELECT id,echo_username,echo_password, notification_email,notification_sms FROM echoalert.accounts WHERE echo_username = %s",(uname))
        res = cur.fetchall()
        cur.close()
        return res


