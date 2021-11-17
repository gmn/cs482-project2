
def DisplayDigitalDisplays():
    """
        (1) Display all the digital displays. For each display, if a user clicks the model no, the detailed model information should be displayed.
    """
    pass


def DisplaysForScheduler(sched):
    """
        (2) Search by inputting a scheduler system. Show the digital displays satisfying the search condition.
    """
    pass


def InsertDisplay(disp):
    """
        (3) Insert a new digital display. When the model of this digital display does not exist, you should design a page to ask users to input the model information first. Display all digital displays after insertion.

    """
    pass


def DeleteDisplay(disp):
    """
        (4) When displaying all digital displays’ information, users can choose one digital display and delete it from the database. For the digital display that needs to be deleted, if none of other digital displays has the same model no, after the digital display is deleted, its corresponding model should also be deleted. Display all digital displays and all models after deletion.

    """
    pass


def UpdateDisplay(disp):
    """
        (5) When displaying all digital displays’ information, users can choose one digital display and update it. Show the information of all digital displays after updating.
    """
    pass


def login_dialog():
    """
    Once users input these information, the
    database should show whether it has connected to the database correctly.
    """
    print('Connected Successfully!')



def main_menu():
    """
    - 1. Display all the digital displays.
    - 2. Search digital displays given a scheduler system
    - 3. Insert a new digital display
    - 4. Delete a digital display
    - 5. Update a digital display
    - 6. Logout
    """
    pass


if __name__ == '__main__':
    """
    prompt users to input database host,
    database name, username and password.
    """
    login_dialog()

    """
    It should list
    options to conduct the Main functions (see below) and to logout. One example of an
    interface can be a list as follows
    """
    main_menu()



