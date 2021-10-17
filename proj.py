#!/usr/bin/python3

import mysql.connector
import os, sys

#
# set these 2 values
#
username = ''
password = ''

# cs482 db server
host = 'dbclass'

class sqlWrapper:
    database = False
    db = False
    cursor = False
    host = False
    username = False
    password = False


    def __init__(self, h, u, p):
        self.db = mysql.connector.connect(
            host = h,
            user = u,
            password = p
        )
        self.host = h
        self.username = u
        self.password = p
        if self.db:
            print('connected successfully')
        else:
            print('failed to connect')
            sys.exit(1)
        self.cursor = self.db.cursor()


    def connect_to_cs482_db(self):
        """
            custom for cs482
        """
        self.database = ''
        # find the database that starts with our name
        self.cursor.execute('show databases')
        for x in self.cursor:
            if self.username in x[0]:
                self.database = x[0]        

        print( 'using database: "{}"'.format(self.database))
        self.cursor.execute('use {};'.format(self.database))


    def query(self, qstring):
        self.cursor.execute(qstring)
        return [x[0] for x in self.cursor]


    def close(self):
        if self.db.is_connected():
            self.cursor.close()
            self.db.close()
            return True
        else:
            return False


def show_tables():
    db = sqlWrapper(host, username, password)
    db.connect_to_cs482_db()
    print('tables found:')
    for table in db.query('show tables'):
        print(' * "{}"'.format(table))
    db.close()


def usage():
    print('usage: {} <number> [argument]'.format(sys.argv[0]))


def problem1(db):
    print('problem 1')

def problem2(db):
    print('problem 2')

def problem3(db):
    print('problem 3')

def problem4(db):
    print('problem 4')

def problem5(db):
    print('problem 5')

def problem6(db):
    print('problem 6')

def problem7(db):
    print('problem 7')

def problem8(db):
    print('problem 8')



def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    db = sqlWrapper(host, username, password)
    db.connect_to_cs482_db()

    if sys.argv[1] == "1":
        problem1(db)
    elif sys.argv[1] == "2":
        problem2(db)
    elif sys.argv[1] == "3":
        problem3(db)
    elif sys.argv[1] == "4":
        problem4(db)
    elif sys.argv[1] == "5":
        problem5(db)
    elif sys.argv[1] == "6":
        problem6(db)
    elif sys.argv[1] == "7":
        problem7(db)
    elif sys.argv[1] == "8":
        problem8(db)
    else:
        print('do not understand: "{}"'.format(sys.argv[1]))

    db.close()

if __name__ == '__main__':
    show_tables()
    main()
