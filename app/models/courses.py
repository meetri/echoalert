'''courses...'''

import sys
import logging
import time
import logging
import psycopg2
import psycopg2.extras
from pgdb import PgDb
from grades import GradeSummary
from assignments import Assignment

class Course(object):

    def __init__(self, data = None ):
        self.data = data
        self.assignments = None
        self.grades = None

    def get_assignments(self, echo ):
        self.assignments = echo.get_course_assignments( self.data['course_name'] )

    def update_assignments(self):

        notify = False
        for assignment in self.assignments:
            a1 = Assignment(self,assignment)

            if a1.find( assignment['title'] ) == None:
                logging.info("Adding new assignment: {}".format(assignment['title']))
                a1.insert()
                notify = True
            else:
                logging.info("Skipping assignment {}, already exists".format(assignment['title']))

        return notify


    def get_grades(self):
        self.grades = GradeSummary.get_grade_summary ( self.data['account_id'], self.data['id'] )
        return self.grades.data

    def insert_grades(self, newgrades ):
        GradeSummary.insert( self.data['account_id'], self.data['id'], newgrades )


    def compare_grades ( self, current, newgrades ):
        diflist = [ "kn","co","ag","progress_all","score","progress_gradable","wr","oral" ]

        if current == None: current = {}
        if newgrades == None: newgrades = {}

        difs = []
        for k in diflist:
            if k not in current or k not in newgrades or current[k] != newgrades[k]:
                difs += [k]

        return difs


    @staticmethod
    def add_courses( account_id, courses ):

        for course in courses:
            savemap = {
                    'account_id': account_id,
                    'status': 1,
                    'created_ts': 'now()',
                    'course_name': course['course'],
                    'course_term': course['term']
                    }
            logging.info("Adding new course: {}".format(course['course']) )
            PgDb.getInstance().insert ( "echoalert.courses", savemap )


    @staticmethod
    def get_courses( account_id ):
        cur = PgDb.getInstance().get_dict_cursor()
        cur.execute("SELECT * FROM echoalert.courses WHERE account_id=%s AND status=1", [ account_id ] )
        res = cur.fetchall()
        cur.close()

        courses = {}
        for course in res:
            courses[course['id']] = Course(course)

        return courses

    def insert(self, mapdata ):
        return PgDb.getInstance().insert ( "echoalert.accounts", mapdata )

