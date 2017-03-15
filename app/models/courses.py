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
from notify import Notifier

class Course(object):

    def __init__(self, data = None ):
        self.data = data
        self.assignments = []
        self.grades = None
        self.assets = None
        self.agenda = None

    def get_todos(self, echo ):
        self.todos = echo.get_course_todos( self.data['course_name'] )
        for todo in self.todos:
            todo['assignment_type'] = Notifier.NOTIFYTYPES["TODO_UPDATE"]
            self.assignments += [Assignment(self,todo)]

    def get_agenda(self, echo ):
        self.agenda = echo.get_agenda( self.data['course_name'] )
        self.agenda['assignment_type'] = Notifier.NOTIFYTYPES["AGENDA_UPDATE"]
        title = self.agenda['title']

        # skip when problem getting agenda, or no new agenda
        if title not in ['Loading...','No agenda']:
            self.assignments += [Assignment(self,self.agenda)]

    def get_assets(self, echo ):
        self.assets = echo.get_course_assets( self.data['course_name'] )
        for asset in self.assets:
            asset['assignment_type'] = Notifier.NOTIFYTYPES["ASSET_UPDATE"]
            self.assignments += [Assignment(self,asset)]


    def update_assignments(self):

        hashlist = ()
        for a in self.assignments:
            hashlist =hashlist + ( a.data['hash'], )

        if len(self.assignments) > 0:
            a = self.assignments[0]
            ret = a.exist_list( hashlist )
            existlist = {}
            for r in ret:
                existlist[r[0]] = True

        notify = []
        for a1 in self.assignments:
            if a1.data['hash'] not in existlist:
                logging.info(u"Adding new assignment: {}".format( a1.data['title']))
                a1.insert()
                notify += [ a1.data["assignment_type"] ]
            else:
                logging.info(u"Skipping assignment {}, already exists".format( a1.data['title']))

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

