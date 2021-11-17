
import os
import time
import json

sleep_time = 0.45


def terminal_size():
    def unix_termsize():
        import fcntl, termios, struct
        h, w, hp, wp = struct.unpack(
            'HHHH',
            fcntl.ioctl(0, termios.TIOCGWINSZ,
                struct.pack('HHHH', 0, 0, 0, 0)
            )
        )
        return h, w
    if os.name == 'nt':
        from lib.terminalsize import get_terminal_size
        return get_terminal_size()
    else:
        return unix_termsize()


def IntQuestion( text ):
    if text[-1] != ' ':
        text = '{} '.format( text )
    val = input( text )
    try:
        i = int( val.lstrip().rstrip() )
        return i
    except:
        return False


def ynQuestion( text, default_action='n' ):
    """
        Returns True for 'Y' or False for 'N'
    """

    suffixen = {'y':'[Y/n]','n':'[y/N]'}
    val = input( '{} {}: '.format(text,suffixen[default_action]) )
    if default_action.lower() == 'y':
        return not(val.upper() == 'N')
    else:
        return val.upper() == 'Y'


def ynqQuestion( text, default_action='n' ):
    """
        Returns True for 'Y', False for 'N', None for 'Q'

        (the extra value: q, allows us to field y/n questions,
         but also quit from inner menus)
    """

    suffix = '[';
    for letter in ('y','n','q'):
        if letter.upper() == default_action.upper():
            suffix += letter.upper() + '/'
        else:
            suffix += letter.lower() + '/'
    suffix = suffix[:-1] + ']'

    val = input( '{} {}: '.format(text, suffix) )

    if not val or len(val) == 0:
        return {'y':True,'n':False,'q':None}.get(default_action.lower(),False)

    if val.upper() == 'Q':
        return None
    return val.upper() == 'Y'



def SubMenu( options, header='', prompt='select>', random_noprompt=False, return_obj=False, custom=False, default=False, exit=True, quit=True, padding=False, return_indexes=False ):
    """
        SubMenu

        - takes a list of menu options
        - prints a header
        - prints an arbitary length list of options
        - handles console window height run-overs
        - adds: e) exit menu, q) quit to main, c) custom input
        - print a 'prompt> '
        - gets input, checks for int or option, loops until exit-condition is met, returns a string
    """

    prompt = prompt.rstrip()
    if default:
        prompt = prompt.replace('>', ' (default: {})>'.format(default) )
    if prompt[-1] != ' ':
        prompt = '{} '.format(prompt)

    padding_rows = padding if padding else 6

    while True:
        if header:
            print( header )

        # prepare for paged print
        term_row_printing = 0
        index_into_dataset = 0
        term_height, _ = terminal_size()

        while index_into_dataset <= len(options):

            if index_into_dataset < len(options):
                option = options[index_into_dataset]

            # terminal screen is full, or at end of list
            if term_row_printing >= ( term_height - padding_rows ) or index_into_dataset >= len(options):
                term_row_printing = 0

                if index_into_dataset < len(options) - 1:
                    print('-------MORE-------')
                else:
                    print('')

                # print the menu and prompt
                if len(options) >= (term_height - padding_rows):
                    print( ' p) show previous screen' )
                if exit:
                    print( ' e) exit to previous menu' )
                if quit:
                    print( ' q) quit' )
                if custom:
                    print( ' c) {}'.format(custom) )

                if index_into_dataset < len(options) - 1:
                    print( '*Enter) Next page' )

                ans = input( prompt ).rstrip().lstrip()
                if ans.lower() == 'p':
                    index_into_dataset = max( index_into_dataset - 2 * ( term_height - padding_rows ), 0 )
                    continue
                elif ans == "":
                    if index_into_dataset == len(options):
                        break
                    else:
                        continue
                else:
                    break

            if type(option) is type({}):
                option = fmt_item( option )
            print( ' {}: "{}"'.format(index_into_dataset, option) )

            term_row_printing = term_row_printing + 1
            index_into_dataset = index_into_dataset + 1

        if custom and ans == 'c':
            while True:
                txt = input( '{}> '.format(custom) )
                if txt:
                    if txt == 'e':
                        return False
                    elif txt == 'q':
                        return None
                    return txt if not return_indexes else 'c'

        if ans == 'e':
            return False
        elif ans == 'q':
            return None
        else:
            if not ans and default:
                return default
            try:
                iv = int(ans)
            except:
                print( 'invalid selection' )
                time.sleep( sleep_time )
                continue
            if iv < 0 or iv >= len(options):
                print( 'out of range' )
                time.sleep( sleep_time )
                continue
            else:
                return iv if return_indexes else options[ iv ]


def edit_string(k, c):
    v = c[k]
    print('\'{}\' currently set to: "{}"'.format(k, v))
    ans = SubMenu(['edit', 'return'], "Select an option")
    if not ans:
        return ans
    if ans == 'return':
        return False
    if ans == 'edit':
        nval = input("enter a new value> ")
        print('\'{}\' set to: "{}"'.format(k, nval))
        c[k] = nval
        return True
    return False


def edit_list(k, c, altName=False):
    changes = 0
    name = altName if altName else k
    while True:
        print('Editing list {}'.format(name))
        ans = SubMenu(c[k]+[' **Add New Item**'], "Select value to edit", return_indexes=True)

        if type(ans) != type(int()) and not ans:
            return changes

        index = int(ans)
        new_item_index = len(c[k])

        if index == new_item_index:
            while True:
                pstr = input("enter path: ")
                c[k].append(pstr)
                changes += 1
                print(json.dumps(c[k], indent='  '))
                if not ynQuestion("Add another path?"):
                    break
            continue

        ans = SubMenu(['Edit', 'Delete'], "Edit or Delete this item?")
        if not ans:
            continue
        if ans == 'Delete':
            v = c[k][index]
            c[k].pop(index)
            changes += 1
            print('"{}" removed'.format(v))
        elif ans == 'Edit':
            nval = input('set to what value> ')
            v = c[k][index]
            c[k][index] = nval
            changes += 1
            print('value "{}" changed to "{}"'.format(v, nval))

    return changes




def nestedMenuDemo():
    attributes = {'height':200, 'width':400, 'weight':100, 'cost':25}
    inventory = ['monitor1', 'monitor2']
    while True:
        actions = [ 'Attributes', 'Inventory' ]
        opt = SubMenu( actions, '\nEdit which category?' )
        if not opt:
            break

        if opt == 'Attributes':
            while True:
                actions = list(attributes.keys())
                atr = SubMenu( actions, '\nEdit which attribute?' )
                if atr is None:
                    return
                if not atr:
                    break
                eans = edit_string(atr, attributes)
                if eans is None:
                    return

        elif opt == 'Inventory':
            print('Showing Inventory: ', end='')
            print(json.dumps(inventory, indent='  '))
            add = ynQuestion('Add Item?')
            if add:
                item = input('Enter New Inventory Item> ')
                if item:
                    inventory.append(item)


if __name__ == '__main__':
    nestedMenuDemo()
