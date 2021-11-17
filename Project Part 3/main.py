
from sql import sqlWrapper
from dialogues import Question, ynQuestion, SubMenu
import sys
import time

def getMaxColWidths(col_widths, data):
    assert(len(col_widths) >= len(data))
    for i,d in enumerate(data):
        if len(str(d)) > col_widths[i]:
            col_widths[i] = len(str(d))


def printHeaderAndResults(header, res, col_widths):
    print()
    if header:
        print_header(col_widths, header)
        print('-' * (sum(col_widths) + len(col_widths)*2))
    if res:
        print_rows(col_widths, res)

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

def fancy_print(header, res, widths):
    getMaxColWidths(widths, header)
    for row in res:
        getMaxColWidths(widths, row)
    printHeaderAndResults(header, res, widths)


def DisplayDigitalDisplays(db):
    """
        (1) Display all the digital displays. For each display, if a user clicks the model no, the detailed model information should be displayed.
    """
    res = db.query("SELECT * FROM DigitalDisplay;")
    header = ['Serial Number', 'Scheduler System', 'Model No.']
    widths = [0, 0, 0]
    fancy_print(header, res, widths)

    print()
    opt = SubMenu(['Lookup Model'], 'If you would like to look up model information. Please use the options below.', exit=False)
    if opt is None:
        return
    if opt == 'Lookup Model':
        modelNo = Question('Model Number> ')
        res = db.query(f'SELECT * FROM Model WHERE modelNo="{modelNo}";')
        header = ['Model No.', 'Width', 'Height', 'Weight', 'Depth', 'Screen Size']
        widths = [0, 0, 0, 0, 0, 0]
        fancy_print(header, res, widths)
    time.sleep(0.5)


def DisplaysForScheduler(db):
    """
        (2) Search by inputting a scheduler system. Show the digital displays satisfying the search condition.
    """
    print()
    schedulerSystem = Question('Scheduler System> ')
    res = db.query(f'SELECT * FROM DigitalDisplay WHERE schedulerSystem="{schedulerSystem}";')
    header = ['Serial Number', 'Scheduler System', 'Model No.']
    widths = [0, 0, 0]
    fancy_print(header, res, widths)
    time.sleep(0.5)


def InsertDisplay(db):
    """
        (3) Insert a new digital display. When the model of this digital display does not exist, you should design a page to ask users to input the model information first. Display all digital displays after insertion.

    """
    print('in InsertDisplay')
    time.sleep(0.5)


def DeleteDisplay(db):
    """
        (4) When displaying all digital displays’ information, users can choose one digital display and delete it from the database. For the digital display that needs to be deleted, if none of other digital displays has the same model no, after the digital display is deleted, its corresponding model should also be deleted. Display all digital displays and all models after deletion.

    """
    print('in DeleteDisplay')
    time.sleep(0.5)


def UpdateDisplay(disp):
    """
        (5) When displaying all digital displays’ information, users can choose one digital display and update it. Show the information of all digital displays after updating.
    """
    print('in UpdateDisplay')
    time.sleep(0.5)


def login_dialog():
    """
    Once users input these information, the
    database should show whether it has connected to the database correctly.
    """
    while True:
        opt = SubMenu(['login'], 'Please login to begin, or quit', exit=False)
        if opt is None:
            db = False
            return db

        if opt == 'login':
            # host, database, username, password
            host = Question( 'To connect, please enter the host> ')
            database = Question( 'To connect, please enter the database> ')
            username = Question( 'To connect, please enter the username> ')
            password = Question( 'To connect, please enter the password> ')

            print('Connecting to MySQL server...')
            db = sqlWrapper(host, database, username, password)
            return db


def main_menu(db):
    """
    - 1. Display all the digital displays.
    - 2. Search digital displays given a scheduler system
    - 3. Insert a new digital display
    - 4. Delete a digital display
    - 5. Update a digital display
    - 6. Logout
    """
    menuopts = [ "Display all the digital displays.",
                 "Search digital displays given a scheduler system",
                 "Insert a new digital display",
                 "Delete a digital display",
                 "Update a digital display",
                 "Logout" ]
    while True:
        opt = SubMenu(menuopts, "\nPlease select an option", exit=False,
                      quit=False, return_indexes=True)
        if opt is None:
            print('quitting..goodbye')
            break
        elif opt == 0:
            DisplayDigitalDisplays(db)
        elif opt == 1:
            DisplaysForScheduler(db)
        elif opt == 2:
            InsertDisplay(db)
        elif opt == 3:
            DeleteDisplay(db)
        elif opt == 4:
            UpdateDisplay(db)
        elif opt == 5:
            print('logging out of mysql')
            time.sleep(0.28)
            if db.close():
                print('database closed successfully')
            else:
                print('error closing db')
            break


if __name__ == '__main__':
    """
    prompt users to input database host,
    database name, username and password.
    """
    db = login_dialog()
    if db:
        if db.is_connected():
            print('** Database has connected correctly')
            time.sleep(.60)
        else:
            print('Warning: Database failed to connect', file=sys.stderr)
            sys.exit(123)
    else:
        sys.exit(0)

    """
    It should list
    options to conduct the Main functions (see below) and to logout. One example of an
    interface can be a list as follows
    """
    main_menu(db)


