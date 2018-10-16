import pymysql
import pymysql.cursors

from django.conf import settings

db = settings.DATABASES
bkdb = db["data_backup"]
cdb = db['default']


class MysqlHandler(object):
    """
    处理mysql语句
    """

    def __init__(self):
        self.db = None
        self.cur = None

    def view_sql(self, db, sql):
        self.connect_db(db)
        try:
            self.cur.execute(sql)
            data = self.cur.fetchall()
            return data
        except Exception as e:
            self.db.rollback()
            return e
        finally:
            self.close_db()

    def do_sql(self, db, sql):
        self.connect_db(db)
        try:
            data = self.cur.execute(sql)
            self.db.commit()
            return data
        except Exception as e:
            self.db.rollback()
            return e
        finally:
            self.close_db()

    def connect_db(self, dbname):
        if dbname == "bkdb":
            self.db = pymysql.connect(
                host=bkdb["HOST"],
                port=int(bkdb["PORT"]),
                user=bkdb["USER"],
                passwd=bkdb["PASSWORD"],
                db=bkdb["NAME"],
                charset="utf8",
            )
        elif dbname == "cdb":
            self.db = pymysql.connect(
                host=cdb["HOST"],
                port=int(cdb["PORT"]),
                user=cdb["USER"],
                passwd=cdb["PASSWORD"],
                db=cdb["NAME"],
                charset="utf8",
            )
        self.cur = self.db.cursor(pymysql.cursors.DictCursor)

    def close_db(self):
        self.cur.close()
        self.db.close()

    def bkdb_all(self):
        db = "bkdb"
        sql = "select table_name, engine, table_rows, " \
              "concat(truncate(data_length/1024/1024,2),'MB') as data_size, " \
              "CONCAT(TRUNCATE(index_length/1024/1024,2),'MB') AS index_size, " \
              "create_time, update_time, " \
              "table_collation, table_comment from tables where table_schema='comics'"
        return self.view_sql(db, sql)

    def show_cdb_create(self, table):
        db = "cdb"
        sql = "show create table %s" % table
        return self.view_sql(db, sql)

    def editor_cdb(self, sql):
        db = "cdb"
        return self.do_sql(db, sql)


datbase = MysqlHandler()
