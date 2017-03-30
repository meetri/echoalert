#!/usr/bin/python -u
import os
import time
import sys
import datetime
import logging
import hashlib

script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_path + "/models")

from pgdb import PgDb
from accounts import Account
from echosite import Echosite
from notify import Notifier

logging.basicConfig( level=logging.INFO)

connInfo = {
        "dbname": os.getenv('DBNAME', "echoalert"),
        "user": os.getenv('DBUSER', "postgres"),
        "host": os.getenv('DBHOST', "localhost"),
        "port": os.getenv('DBPORT', "5432"),
        "password": os.getenv('DBPASS', "defaultpassword"),
        }

print connInfo

print "connecting to db"
PgDb.setup( **connInfo)

print "getting active users"
accounts = Account.get_user_paginate(0,100)

print "loading scraper"
echo = Echosite()

for account in accounts:

    echo.login( account.data['echo_site'],account.data['echo_username'],account.data['echo_password'] )

    courses = account.get_courses()
    if len(courses) == 0:
        logging.info("adding new account... getting courses")
        account.add_courses( echo.get_courses() )
        courses = account.get_courses()

    echo_summary = echo.get_grade_summary()

    notifications = []
    for course_id,course in courses.iteritems():

        course.get_agenda( echo )
        course.get_assets( echo )
        course.get_todos( echo )

        notify = course.update_assignments()
        if len(notify) > 0:
            notifications += notify

        newgrades = Echosite.filter_course_grades ( course.data['course_name'],echo_summary )
        dif = course.compare_grades ( course.get_grades() , newgrades )
        if len(dif) > 0:
            logging.info("updating grades for {}".format ( course.data['course_name'] ))
            course.insert_grades( newgrades )
            notifications += [ Notifier.NOTIFYTYPES["GRADE_UPDATE"] ]
        else:
            logging.info("{} grades up to date".format(course.data['course_name']))

    for notify_id in set(notifications):
        print "Sending notification type {}".format(notify_id)
        account.notify( notify_id )


    logging.info("completed with this account")
    echo.browser.close()


echo.browser.quit()
