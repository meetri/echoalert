'''grade_summary model'''

import sys
import time
import logging
import psycopg2
import psycopg2.extras
from pgdb import PgDb

class GradeSummary(object):

    def __init__(self,data):
        self.data = data

    @staticmethod
    def compare_grades_after( account_id, date ):
        cur = PgDb.getInstance().get_dict_cursor()
        cur.execute("""
SELECT C.course_name,p.score FROM echoalert.grade_summary AS GS1
JOIN LATERAL (
    SELECT * FROM echoalert.grade_summary AS GS
    WHERE GS.account_id=%s AND GS.course_id = GS1.course_id
    ORDER BY GS.created_ts DESC LIMIT 2) p on true
JOIN echoalert.courses AS C ON C.id=GS1.course_id
WHERE GS1.account_id=%s
AND GS1.created_ts > %s::timestamp - interval '5 min'""",(account_id,account_id,date) )

        res = cur.fetchall()
        cur.close()
        return res


    @staticmethod
    def get_grade_summary ( account_id, course_id ):
        cur = PgDb.getInstance().get_dict_cursor()
        cur.execute("SELECT * FROM echoalert.grade_summary WHERE account_id=%s AND course_id=%s ORDER BY created_ts DESC limit 1",(account_id,course_id) )
        res = cur.fetchone()
        cur.close()

        return GradeSummary( res )


    @staticmethod
    def get_grade_summaries(account_id):
        cur = PgDb.getInstance().get_dict_cursor()
        cur.execute("with lastrecord AS ( SELECT groupset FROM echoalert.grade_summary WHERE account_id=%s ORDER by created_ts desc LIMIT 1) SELECT gs.* FROM lastrecord AS l JOIN echoalert.grade_summary AS gs ON gs.groupset = l.groupset",[ account_id ])
        res = cur.fetchall()
        cur.close()

        return res

        '''
        out = []
        for grade in res:
            out += [ GradeSummary(grade) ]

        return out
        '''


    @staticmethod
    def insert( account_id, course_id, mapdata ):

        save = mapdata.copy()
        save['account_id'] = account_id
        save['course_id'] = course_id
        save['created_ts'] = 'now()'
        if 'course' in save:
            save.pop('course',None)

        PgDb.getInstance().insert ( "echoalert.grade_summary", save)

