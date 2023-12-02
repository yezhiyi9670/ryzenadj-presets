from sys import argv
import os
import ctypes
from plyer import notification
import time

myname = 'ryzenadj-preset'

def is_admin():
    is_admin = False
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

command = None

dir_base = os.path.dirname(__file__)
dir_presets = os.path.join(dir_base, 'presets')
dir_set = os.path.join(dir_base, 'set')
file_current = os.path.join(dir_set, 'current.txt')

if not os.path.exists(file_current):
    os.makedirs(dir_set, 511, True)
    open(file_current, 'w', encoding='utf-8').write('none')

current_mode = open(file_current, 'r', encoding='utf-8').read().strip()
file_mode = os.path.join(dir_presets, current_mode + '.txt')
current_mode_exists = os.path.exists(file_mode)

if len(argv) > 1:
    command = argv[1]

def apply_preset(name):
    file_mode = os.path.join(dir_presets, name + '.txt')
    if not os.path.exists(file_mode):
        return -1
    return os.system(open(file_mode, 'r', encoding='utf-8').read().strip())

if command != None and command != 'current' and not is_admin():
    print('This command can only be used by Administrators.')
    exit(5)

if command == None:
    print('Current preset:', current_mode + (' (non-existent)' if not current_mode_exists else ''))
elif command == 'current':
    print(current_mode)
elif command == 'switch':
    if len(argv) <= 2:
        print('Usage: ' + myname + ' switch <mode>')
        exit(3)
    current_mode = argv[2]
    if current_mode.find('..') != -1:
        print('Usage: Illegal mode name `' + current_mode + '`')
        exit(3)
    file_mode = os.path.join(dir_presets, current_mode + '.txt')
    current_mode_exists = os.path.exists(file_mode)
    if current_mode_exists:
        open(file_current, 'w', encoding='utf-8').write(current_mode)
        print('Switched to preset `' + current_mode + '`, applying:')
        ch = apply_preset(current_mode)
        if ch == 0:
            notification.notify(
                title = 'RyzenAdj Presets',
                message = 'Successfully applied `' + current_mode + '`',
                app_icon = None,
                timeout = 2,
            )
        else:
            notification.notify(
                title = 'RyzenAdj Presets',
                message = 'Failed to apply `' + current_mode + '`',
                app_icon = None,
                timeout = 2,
            )
        exit(ch)
    else:
        print('Preset `' + current_mode + '` does not exist')
        exit(4)
elif command == 'reapply':
    do_loop = True
    loop_count = 0
    while do_loop:
        do_loop = False
        if current_mode_exists:
            print('Applying preset `' + current_mode + '`:')
            ch = apply_preset(current_mode)
            if ch != 0:
                notification.notify(
                    title = 'RyzenAdj Presets',
                    message = 'Failed to reapply `' + current_mode + '`',
                    app_icon = None,
                    timeout = 2,
                )
            else:
                prev_mode = current_mode
                # Reload current mode specification
                current_mode = open(file_current, 'r', encoding='utf-8').read().strip()
                file_mode = os.path.join(dir_presets, current_mode + '.txt')
                current_mode_exists = os.path.exists(file_mode)
                if current_mode != prev_mode:
                    do_loop = True
                    print('Current mode has changed. Reapplying once more...')
            if not do_loop:
                exit(ch)
        else:
            print('Preset `' + current_mode + '` does not exist')
            exit(4)
        loop_count += 1
        if loop_count >= 5:
            exit(-1)
else:
    print('Usage:')
    print('  ' + myname + '  # prints the current preset')
    print('  ' + myname + ' current  # prints the current preset name in raw')
    print('  ' + myname + ' switch <mode>  # switch to another mode')
    print('  ' + myname + ' reapply  # reapply current mode')
    exit(3)
