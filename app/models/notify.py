'''notifications'''

import sys
import time
import psycopg2
import psycopg2.extras
from pgdb import PgDb

class Notifier(object):

    NOTIFYTYPES = {
            "GRADE_UPDATE" : 1,
            "TODO_UPDATE" : 2,
            "COURSE_UPDATE" : 3,
            "AGENDA_UPDATE" : 4,
            "ASSET_UPDATE" : 5,
            "SAYING_HI" : 6
            }

    def __init__(self,data):
        self.data = data

    @staticmethod
    def get_recent_grades(  account_id ):
        return 1

    @staticmethod
    def get_recent_agenda(  account_id ):
        return 1


    @staticmethod
    def mark_sent( notify_id, msg ):
        cur = PgDb.getInstance().get_dict_cursor()
        cur.execute("UPDATE echoalert.notifications SET status=1,status_message=%s, sent_ts=now() WHERE id=%s",[msg,notify_id])
        res = PgDb.getInstance().conn.commit()
        cur.close()
        return res



    @staticmethod
    def get_new_notices():
        cur = PgDb.getInstance().get_dict_cursor()
        cur.execute("""SELECT N.id, AC.notification_email, AC.notification_sms,N.account_id,N.notification_type,N.created_ts
        FROM echoalert.notifications AS N JOIN echoalert.accounts AS AC on AC.id=N.account_id
        WHERE N.status=0 AND AC.enabled=true ORDER BY N.created_ts ASC""")
        res = cur.fetchall()
        cur.close()
        return res


    @staticmethod
    def insert( account_id, notifyType, notifydate ):

        save = {}
        save['account_id'] = account_id
        save['status'] = 0
        save['notification_type'] = notifyType
        save['created_ts'] = notifydate

        return PgDb.getInstance().insert ( "echoalert.notifications", save)

