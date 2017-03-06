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

logging.basicConfig( level=logging.INFO)

connInfo = {
        "dbname": os.getenv('DBNAME', "echoalert"),
        "user": os.getenv('DBUSER', "postgres"),
        "host": os.getenv('DBHOST', "localhost"),
        "port": os.getenv('DBPORT', "5432"),
        "password": os.getenv('DBPASS', "defaultpassword"),
        }

PgDb.setup( **connInfo)
accounts = Account.get_user_paginate(0,100)
echo = Echosite()

for account in accounts:

    echo.login( account.data['echo_site'],account.data['echo_username'],account.data['echo_password'] )

    courses = account.get_courses()
    if len(courses) == 0:
        logging.info("adding new account... getting courses")
        account.add_courses( echo.get_courses() )
        courses = account.get_courses()

    echo_summary = echo.get_grade_summary()

    notify_grades = False
    notify_assignments = False
    for course_id,course in courses.iteritems():

        course.get_assignments( echo )
        if course.update_assignments():
            notify_assignments = True

        newgrades = Echosite.filter_course_grades ( course.data['course_name'],echo_summary )
        dif = course.compare_grades ( course.get_grades() , newgrades )
        if len(dif) > 0:
            logging.info("updating grades for {}".format ( course.data['course_name'] ))
            course.insert_grades( newgrades )
            notify_grades = True;
        else:
            logging.info("{} grades up to date".format(course.data['course_name']))

    if notify_grades:
        logging.info("sending grade update notification")
        account.notify ( "GRADE_UPDATE" )

    if notify_assignments:
        logging.info("sending assignment update notification")
        account.notify ( "ASSIGNMENT_UPDATE" )

    logging.info("completed with this account")
    echo.browser.close()


echo.browser.quit()
