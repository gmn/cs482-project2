#!/usr/bin/python3

import mysql.connector
import os, sys

############################################
#
# Set these 2 values and everything else will work.
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
        # https://stackoverflow.com/questions/38350816/python-mysql-connector-internalerror-unread-result-found-when-close-cursor
        self.cursor = self.db.cursor(buffered=True)

    def connect_to_cs482_db(self):
        """
            custom for cs482

            Atomatically determines the name of your database
            and connects to it. So that way, everything is driven
            off of the username field set at the top of this file. 
        """
        self.database = ''
        # find the database that starts with our name
        self.cursor.execute('show databases;')
        for x in self.cursor:
            if x[0].startswith(self.username):
                self.database = x[0]        
                # if cursor not set buffered=True, you must read the entire
                # cursor or else it throws an error, idiotic
                break

        print( 'using database: "{}"'.format(self.database))
        self.cursor.execute('use {}'.format(self.database))

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
        fmt = '{0:<' + str(widths[i]+2) + '}'
        print(fmt.format(field), end='')
    print()


def print_rows(widths, rows):
    for row in rows:
        for i, col in enumerate(row):
            fmt = '{0:<' + str(widths[i]+2) + '}'
            print(fmt.format(col), end='')
        print()


def headerWidths(header):
    # init widths to all zeros, one for each column
    col_widths = [0 for _ in range(len(header))]
    # get the max widths for the header names
    getMaxColWidths(col_widths, header)
    return col_widths


def getMaxColWidths(col_widths, data):
    assert(len(col_widths) >= len(data))
    for i,d in enumerate(data):
        if len(str(d)) > col_widths[i]:
            col_widths[i] = len(d)

def printHeaderAndResults(header, res, col_widths):
    print()
    if header:
        print_header(col_widths, header)
        print('-' * (sum(col_widths) + len(col_widths)*2))
    if res:
        print_rows(col_widths, res)


def problem1(db):
    """
        PROBLEM 1 - 

        This is supposed to match a substring against the street in a case sensitive manner. I don't think the sql LIKE operator is case-sensitive, so we have to do it ourselves in code.
    """
    print(f'\nproblem 1 - showing sites with address containing "{sys.argv[2]}"\n')

    # get list of tuples with column names 
    header = [x[0] for x in db.query('describe Site;')]

    # init widths to all zeros, one for each column
    col_widths = headerWidths(header)

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
    printHeaderAndResults(header, res, col_widths)


def problem2(db):
    """
        Find the digital displays with a given scheduler system. Show their serial nos, model nos, and the names of technical supports who specialize their models. The scheduler system should be a parameter input through the main program. To get the answer of this question, the command to run is

    """
    print('problem 2 - find digital displays and name of technician who support a model with a given schedulersystem')

    res = db.query("SELECT D.serialNo, D.modelNo, T.name from DigitalDisplay as D, TechnicalSupport as T, Specializes as S  WHERE ( S.empId = T.empId AND D.modelNo = S.modelNo) AND D.schedulerSystem = '{}';".format(sys.argv[2]))
    widths = [0, 0, 0]
    header = ['Serial Number', 'Model Number', 'Name']
    getMaxColWidths(widths, header)
    for row in res:
        getMaxColWidths(widths, row)
    printHeaderAndResults(header, res, widths)


def problem3(db):
    """
        List the distinct names of all salesmen and the number of salesmen with that name.
    """
    print('problem 3')

    names = db.query("select distinct name from Salesman order by name ASC;")
    outs = []
    for name in names:
        cnts = db.query("select count(*) as cnt from Salesman where name = '{}';".format(name))
        outs.append((name, cnts[0]))

    header = ['Name', 'cnt']
    widths = headerWidths(header)
    for row in outs:
        getMaxColWidths(widths, row)

    # print just the header
    printHeaderAndResults(header, None, widths)
    
    for row in outs:
        fmt = '{0:<' + str(widths[0]+2) + '}'
        print(fmt.format(row[0]), end='')
        fmt = '{0:<' + str(widths[1]+2) + '}'
        print(fmt.format(row[1]), end='')
        if int(row[1]) > 1:
            res = db.query("select * from Salesman where name = '{}';".format(row[0]))
            print(", ".join([i for i in map(str, res)]))
        else:
            print()


def problem4(db):
    print('problem 4 - Finds the clients with a given input phone number')

    # header info
    header = [x[0] for x in db.query('describe Client')]

    # column widths for each table field
    widths = headerWidths(header)

    # query
    res = db.query(f'SELECT * FROM Client WHERE phone = "{sys.argv[2]}";')

    # update the widths for printing
    for row in res:
        getMaxColWidths(widths, row)

    # print answer
    printHeaderAndResults(header, res, widths)


def problem5(db):
    """
    Find the total working hours of each administrator. Display the administrators’ employee ids, names, and total working hours in ascending order of the total working hours
    """
    print('problem 5 - Find the total working hours of every administrator')

    res = db.query('SELECT A.empId, A.name, TotalHours.T FROM Administrator as A NATURAL JOIN (SELECT empId, SUM(hours) as T FROM AdmWorkHours GROUP BY empId) as TotalHours ORDER by TotalHours.T ASC;')

    header = ['employee id', 'name', 'total working hours']
    widths = headerWidths(header)
    for row in res:
        getMaxColWidths(widths, row)
    # print answer
    printHeaderAndResults(header, res, widths)


def problem6(db):
    print('problem 6 - Find the technical support who specalize in a specific model')

    res = db.query(f'SELECT T.name FROM TechnicalSupport as T NATURAL JOIN Specializes as S WHERE S.modelNo = "{sys.argv[2]}"')

    print(res)

def problem7(db):
    print('problem 7 - Shows the salesman in decending order based on their commission rate')

    res = db.query('SELECT S.name, ComAvg.AVRG FROM Salesman as S NATURAL JOIN (SELECT empId, AVG(commissionRate) as AVRG FROM Purchases GROUP BY empId) as ComAvg ORDER BY ComAvg.AVRG DESC')

    print(res)


def problem8(db):
    print('problem 8 - Displays the number of Administrators, Salesman, and Technicians')

    res = db.query('SELECT A.cnt, B.cnt, C.cnt FROM (SELECT count(empId) as cnt from Administrator) as A, (SELECT count(empId) as cnt from Salesman) as B, (SELECT count(empId) as cnt from Salesman) as C')

    print(res)


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
