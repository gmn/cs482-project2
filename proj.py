#!/usr/bin/python3

import mysql.connector
import os, sys

############################################
#
# set these 2 values!!!
#
############################################
username = ''
password = ''
############################################

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

            Atomatically determines the name of your database
            and connects to it. So that way, everything is driven
            off of the username field set at the top of this file. 
        """
        self.database = ''
        # find the database that starts with our name
        self.cursor.execute('show databases')
        for x in self.cursor:
            if x[0].startswith(self.username):
                self.database = x[0]        
                break

        print( 'using database: "{}"'.format(self.database))
        self.cursor.execute('use {};'.format(self.database))

    def query(self, qstring):
        self.cursor.execute(qstring)
        return [x[0] if len(x) == 1 else x for x in self.cursor]

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


def print_header(widths, header):
    for i, field in enumerate(header):
        fmt = '{0:<' + str(widths[i]+1) + '}'
        print(fmt.format(field), end='')
    print()


def print_rows(widths, rows):
    for row in rows:
        for i, col in enumerate(row):
            fmt = '{0:<' + str(widths[i]+1) + '}'
            print(fmt.format(col), end='')
        print()


def getMaxColWidths(col_widths, data):
    assert(len(col_widths) >= len(data))
    for i,d in enumerate(data):
        if len(str(d)) > col_widths[i]:
            col_widths[i] = len(d)


def problem1(db):
    """
        note: this is supposed to match the street and be case sensitive. I don't think the sql LIKE operator is case-sensitive, so probably need to fix that, or do the match against all the rows by hand. Not sure what they want.
    """
    print(f'\nproblem 1 - showing sites with address containing "{sys.argv[2]}"\n')

    # get list of tuples with column names 
    header = db.query('describe Site;')
    header = [x[0] for x in header]

    # init widths to all zeros, one for each column
    col_widths = [0 for _ in range(len(header))]

    # get the max widths for the header names
    getMaxColWidths(col_widths, header)

    # do the problem1 query
    res = db.query(f'select * from Site where address like "%{sys.argv[2]}%";')

    # filter res by case-sensitive matching against argv[2]
    res2 = []
    for row in res:
        if sys.argv[2] in row[2]:
            res2.append(row)
    res = res2

    # get max widths for each column of each row
    for row in res:
        getMaxColWidths(col_widths, row)

    ##
    ## Ok, now that we have correct widths, we can format the output nicely
    ##
    print_header(col_widths, header)
    print('-' * (sum(col_widths) + len(col_widths)))
    print_rows(col_widths, res)


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

    # connect to the database
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

    # close database connection
    db.close()


if __name__ == '__main__':
    #show_tables()
    main()
