
import json
from sql import sqlWrapper
from dialogues import Question, ynQuestion, ynqQuestion, SubMenu
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

def fancy_print(header, res):
    widths = [0 for _ in header]
    getMaxColWidths(widths, header)
    for row in res:
        getMaxColWidths(widths, row)
    printHeaderAndResults(header, res, widths)


def ShowDigitalDisplays(db):
    res = db.query('SELECT * from DigitalDisplay;')
    headers = ['Serial Number', 'Scheduler System', 'Model Number']
    print("Digital Displays", end='')
    fancy_print(headers, res)


def ShowModels(db):
    res = db.query('SELECT * from Model;')
    headers = ['modelNo', 'width', 'height', 'weight', 'depth', 'screensize']
    print('Models', end='')
    fancy_print(headers, res)


def DisplayDigitalDisplays(db):
    """
        (1) Display all the digital displays. For each display, if a user clicks the model no, the detailed model information should be displayed.
        (5) When displaying all digital displays’ information, users can choose one digital display and update it. Show the information of all digital displays after updating.
    """
    res = db.query("SELECT * FROM DigitalDisplay;")
    header = ['Serial Number', 'Scheduler System', 'Model No.']
    fancy_print(header, res)

    print()
    opt = SubMenu(['Lookup Model', 'Update Display'], 'If you would like to look up model information, or update display information. Please use the options below.', quit=False)
    if opt is None:
        return
    if opt == 'Lookup Model':
        while True:
            modelNo = SubMenu([i[2] for i in res], 'Select Model Number to Look up', quit=False)
            if not modelNo:
                break
            res2 = db.query(f'SELECT * FROM Model WHERE modelNo="{modelNo}";')
            header = ['Model No.', 'Width', 'Height', 'Weight', 'Depth', 'Screen Size']
            fancy_print(header, res2)
    if opt == 'Update Display':
        while True:
            updateDisp = SubMenu([i[0] for i in res], 'Select Display to Update', quit=False)
            for item in res:
                if item[0] == updateDisp:
                    newSerialNo = item[0]
                    newScheduler = item[1]
            if not updateDisp:
                break
            serialNo = Question('Enter New Serial Number (Leave Black for No Update)> ')
            if serialNo != '':
                newSerialNo = serialNo
            scheduler = Question('Enter New Scheduler System (Leave Black for No Update)> ')
            if scheduler != '':
                newScheduler = scheduler
            db.update(f'UPDATE DigitalDisplay SET serialNo="{newSerialNo}", schedulerSystem="{newScheduler}" WHERE serialNo="{updateDisp}"')
            res2 = db.query("SELECT * FROM DigitalDisplay;")
            header = ['Serial Number', 'Scheduler System', 'Model No.']
            fancy_print(header, res2)
        
    time.sleep(0.5)


def DisplaysForScheduler(db):
    """
        (2) Search by inputting a scheduler system. Show the digital displays satisfying the search condition.
    """
    print()
    schedulerSystem = Question('Scheduler System> ')
    res = db.query(f'SELECT * FROM DigitalDisplay WHERE schedulerSystem="{schedulerSystem}";')
    header = ['Serial Number', 'Scheduler System', 'Model No.']
    fancy_print(header, res)
    time.sleep(0.5)


def InsertDisplay(db):
    """
        (3) Insert a new digital display. When the model of this digital display does not exist, you should design a page to ask users to input the model information first. Display all digital displays after insertion.

    """
    # - insert a display, y/n
    ans = ynQuestion('Insert a new display? ')
    if not ans:
        return
    # - enter model number,
    print("Create new Digital Display:")
    modelNo = Question('modelNo> ')
    res = db.query(f'SELECT * from Model where modelNo = "{modelNo}";')
    #   - if model doesn't exist, add a new model
    model = {'modelNo':modelNo,
             'width':0.0,
             'height':0,
             'weight':0,
             'depth':0,
             'screenSize':0}
    if not res:
        print("Model doesn't exist. Please create a new model:")
        for field in model.keys():
            if field == 'modelNo':
                print(f'modelNo> {modelNo}')
                time.sleep(0.6)
            else:
                ans = Question(f'{field}> ')
                model[field] = str(ans)
        db.query('INSERT INTO Model VALUES ("{}",{},{},{},{},{});'.format( *model.values() ))
        print(f'Model {modelNo} created')
        time.sleep(0.3)
        print('Continue creating new display')
        time.sleep(0.3)

    # - finish entering new display
    disp = {'serialNo':0, 'schedulerSystem':0, 'modelNo': modelNo}
    print(f'modelNo> {modelNo}')
    time.sleep(0.5)
    disp['serialNo'] = Question('serialNo> ')
    disp['schedulerSystem'] = Question('schedulerSystem (Random, Smart, or Virtue)> ')
    db.query('INSERT INTO DigitalDisplay VALUES ("{}","{}","{}");'.format(
        *disp.values()))
    print(f'Digital Display {disp["serialNo"]} created.')

    # - show all displays when youre done
    ShowDigitalDisplays(db)
    time.sleep(0.5)


def DeleteDisplay(db):
    """
        (4) When displaying all digital displays’ information, users can choose one digital display and delete it from the database. For the digital display that needs to be deleted, if none of other digital displays has the same model no, after the digital display is deleted, its corresponding model should also be deleted. Display all digital displays and all models after deletion.
    """

    while True:
        res = db.query('SELECT * from DigitalDisplay;')
        if not res:
            print('no displays found')
            return
        # join these together
        displays = [" ".join(e) for e in res]
        which = SubMenu(displays, "Select a display to delete", return_indexes=True, quit=False)
        if type(which) != type(int()):
            return

        print('deleting display {}, serial number: "{}"'.format(which, res[which][0]))
        serialNo = res[which][0]
        modelNo = res[which][2]
        db.query(f'DELETE FROM DigitalDisplay where serialNo = "{serialNo}";')
        time.sleep(1)

        # check if any are left with same model
        mres = db.query(f'SELECT * FROM DigitalDisplay where modelNo = "{modelNo}";')
        if not mres:
            # remove the model if none use it
            print(f'Removing modelNo {modelNo} from list of Models')
            db.query(f'DELETE FROM Model where modelNo = "{modelNo}";')

        # all displays
        print()
        ShowDigitalDisplays(db)
        print()
        time.sleep(1)

        # all models
        ShowModels(db)
        time.sleep(0.5)

        again = ynQuestion("\nDelete another? ")
        if not again:
            break


def UpdateDisplay(disp):
    """
        
    """
    
    time.sleep(0.5)


def login_dialog():
    """
    Once users input these information, the
    database should show whether it has connected to the database correctly.
    """
    while True:
        opt = SubMenu(['login'], """
*******************************************************\n
This is an example database program for cs482 Project 3\n
*******************************************************\n
Please login to begin, or quit.""", exit=False)
        if opt is None:
            return False

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
                 "Show all models.",
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
            ShowModels(db)
        elif opt == 2:
            DisplaysForScheduler(db)
        elif opt == 3:
            InsertDisplay(db)
        elif opt == 4:
            DeleteDisplay(db)
        elif opt == 5:
            UpdateDisplay(db)
        elif opt == 6:
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
    try:
        with open('./credentials', 'r') as f:
            deets = json.load(f)
        print(f'using found credentials: {deets}')
        db = sqlWrapper(*deets)
        if db.is_connected():
            print('>>>>>>>>>>>>using fake login<<<<<<<<<<<<')
            time.sleep(1.0)
    except:
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


