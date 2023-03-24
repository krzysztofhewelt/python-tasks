import pymysql
from pymysql import Connection as MysqlConn


class Database:
    def __init__(self, db, host='localhost', user='root', password=''):
        self.db = db
        self.host = host
        self.user = user
        self.password = password

    def conn(self):
        conn = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.db, port=3306)
        return conn

    def execute(self, sql):
        ok = False
        try:
            conn = self.conn()
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            ok = True
        except pymysql.connect.Error as error:
            print("error", error)
        finally:
            if conn.ping():
                cur.close()
                conn.close()
        return ok

    def get_array(self, sql):
        return