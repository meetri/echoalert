'''access echo grade detils'''
class Accounts(object):

    def __init__(self, dbconn):
        self.dbconn = dbconn


    def get_user_paginate ( self , start,limit ):
        cur = self.dbconn.cursor()
        cur.execute("SELECT id,echo_username,echo_password, notification_email,notification_sms FROM echoalert.accounts ORDER BY id asc offset %d limit %d",(start,limit))
        return cur

    def get_user_by_id ( self , id ):
        cur = self.dbconn.cursor()
        cur.execute("SELECT id,echo_username,echo_password, notification_email,notification_sms FROM echoalert.accounts WHERE id = %d",(id))
        return cur

    def get_user_by_username ( self , uname ):
        cur = self.dbconn.cursor()
        cur.execute("SELECT id,echo_username,echo_password, notification_email,notification_sms FROM echoalert.accounts WHERE echo_username = %s",(uname))
        return cur

