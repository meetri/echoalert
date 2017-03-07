'''assignments...'''

import sys
import time
import psycopg2
import psycopg2.extras
import hashlib
from pgdb import PgDb
from datetime import datetime

class Assignment(object):

    def __init__(self, course, data ):
        self.course = course
        self.data = data

        k = "{}-{}-{}-{}".format(data['assignment_type'],course.data['id'],data['due'],data['title'].encode('ascii','ignore'))
        self.data['hash'] = hashlib.md5(k).hexdigest()
        #print "key = {} hash = {} ".format(k,self.data['hash'])
        #sys.exit()


    def exist_list(self, hashtuple ):
        cur  = PgDb.getInstance().get_dict_cursor()
        cur.execute("SELECT hash FROM echoalert.assignments WHERE account_id=%s AND course_id=%s AND hash IN %s",[self.course.data['account_id'],self.course.data['id'],hashtuple])
        res = cur.fetchall()
        cur.close()
        return res


    def exists( self ):
        cur = PgDb.getInstance().get_dict_cursor()
        cur.execute("SELECT id FROM echoalert.assignments WHERE account_id=%s AND course_id=%s AND title=%s AND due=%s AND assignment_type=%s",[ self.course.data['account_id'],self.course.data['id'],self.data['title'],self.data['due'],self.data['assignment_type']])
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
        mapdata['assignment_type'] = self.data['assignment_type']
        mapdata['account_id'] = self.course.data['account_id']
        mapdata['course_id'] = self.course.data['id']
        mapdata['due_date'] = self.parse_due_date ( self.data['due'] )
        mapdata['created_ts'] = 'now()'
        mapdata['completed'] = False

        return PgDb.getInstance().insert ( "echoalert.assignments", mapdata )
