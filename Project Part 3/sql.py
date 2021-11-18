import mysql.connector
import sys

class sqlWrapper:
    def __init__(self, h, d, u, p):
        self.db = mysql.connector.connect(
            host = h,
            user = u,
            password = p
        )
        self.host = h
        self.database = d
        self.username = u
        self.password = p
        if not self.db.is_connected():
            sys.exit(1)
        # https://stackoverflow.com/questions/38350816/python-mysql-connector-internalerror-unread-result-found-when-close-cursor
        self.cursor = self.db.cursor(buffered=True)
        self.cursor.execute('use {}'.format(self.database))


    def is_connected(self):
        return self.db.is_connected()


    def query(self, qstring):
        self.cursor.execute(qstring)
        self.db.commit()
        return [x[0] if len(x) == 1 else x for x in self.cursor]


    def close(self):
        if self.db.is_connected():
            self.cursor.close()
            self.db.close()
            assert(not self.db.is_connected())
            return True
        else:
            return False


