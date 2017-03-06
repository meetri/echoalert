'''assignments...'''

import sys
import time
import psycopg2
import psycopg2.extras
from pgdb import PgDb
from datetime import datetime

class Assignment(object):

    def __init__(self, course = None, data = None ):
        self.course = course
        self.data = data


    def get_assignments(self):
        cur  = PgDb.getInstance().get_dict_cursor()
        cur.execute("SELECT * FROM echoalert.assignments WHERE account_id=%s AND course_id=%s AND completed=false",[self.course.data['account_id'],self.course.data['id']])
        res = cur.fetchall()
        cur.close()
        return res


    def find( self, title ):
        cur = PgDb.getInstance().get_dict_cursor()
        cur.execute("SELECT * FROM echoalert.assignments WHERE account_id=%s AND course_id=%s AND title=%s",[ self.course.data['account_id'],self.course.data['id'],title])
        res = cur.fetchone()
        cur.close()
        return res


    def parse_due_date(self, datestr ):

        now = datetime.now()
        past_due = False
        datestr = datestr.lower()
        if "past due" in datestr:
            past_due = False
            datestr = datestr.replace("past due: ","")


        # Wed 02/15 2:30 PM
        datetypes = ("%a %m/%d %I:%M %p - %Y","%a %m/%d - %Y")
        datestr = "{} - {}".format(datestr,now.year)

        for dt in datetypes:
            try:
                return datetime.strptime(datestr , dt)
            except:
                continue

        return None


    def insert( self):
        mapdata = self.data.copy()
        mapdata['account_id'] = self.course.data['account_id']
        mapdata['course_id'] = self.course.data['id']
        mapdata['due_date'] = self.parse_due_date ( self.data['due'] )
        mapdata['created_ts'] = 'now()'
        mapdata['completed'] = False
        return PgDb.getInstance().insert ( "echoalert.assignments", mapdata )
