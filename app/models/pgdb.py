import psycopg2

class PgDb(object):

    _instance = None

    def __init__(self,dbname,user,host,port,password):
        self.conn = None
        self.dbname = dbname
        self.user = user
        self.host = host
        self.port = port
        self.password = password
        #self.dbname = "echoalert"
        #self.user = "postgres"
        #self.host = "192.168.59.104"
        #self.port = "32768"
        #self.password = "abignewworld"


    @staticmethod
    def getInstance():
        if PgDb._instance == None:
            PgDb._instance = PgDb()
            PgDb._instance.connect()

        return PgDb._instance


    @staticmethod
    def setup(dbname,user,password,host="localhost",port="5432"):
        PgDb._instance = PgDb(dbname,user,host,port,password)
        PgDb._instance.connect()


    def connect(self):
        try:
            self.conn = psycopg2.connect("dbname='%s' user='%s' host='%s' port='%s' password='%s'" % (self.dbname,self.user,self.host,self.port,self.password))
        except:
            print "failed to connect to db"
            self.conn = None

    def get_dict_cursor(self):
        return self.conn.cursor(cursor_factory= psycopg2.extras.DictCursor )

    def get_cursor(self):
        return self.conn.cursor()

    def insert(self,  schema, mapdata ):
        cur = self.conn.cursor()

        values =  sql = ""
        vdata = []
        for k,v in mapdata.iteritems():
            sql += "{},".format( k )
            values += "%s,"
            vdata += [v]

        sql = "INSERT INTO {} ( {} ) VALUES ( {} )".format(schema, sql[0:-1],values[0:-1])

        cur.execute(sql,vdata)
        res = self.conn.commit()
        cur.close()
        return res

