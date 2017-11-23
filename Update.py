#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
import time
from distutils.version import StrictVersion
from subprocess import check_output
from urllib import urlopen

'''
    ## File written in Python 2.7
    ## This update file program is mainly to :
    1. Set up connection from client to server via http
    2. Download and start the running background program __mainfile__
    3. Download setting file __setting__ for __mainfile__
    4. Update __mainfile__ & __setting__ if the version is higher in **Server**/`config.csv` and `config.csv` & `file`'s version matches

    - Note that in __mainfile__ commands **MUST NOT EXECUTE in IMPORTING** ( in the `check_output_cmd` we import __version__ from __mainfile__ )
    - Version setting is controled by `StrictVersion` so should be set carefully in furthur __mainfile__ setting
    ---
    ## Run code:
     - On server side Terminal, first change to the desired directory then insert :
    `$ python -m SimpleHTTPServer 8000`
     - On client side Terminal:
    `$ python Update.py`
'''

############ Initial Setting ############
MAC = 'XX.XXX.XX.XXX'                   #
PORT = '8000'                           #
__configuration__ = 'config.csv'        #
__mainfile__ = 'Toy.py'                 #
__setting__ = 'Toy_setting.csv'         #
#########################################

######################################################################################################
csv_get_url = 'http://' + MAC + ':' + PORT + '/' + 'Server/' + __configuration__
main_file_get_url = 'http://' + MAC + ':' + PORT + '/' + 'Server/' + __mainfile__
setting_get_url = 'http://' + MAC + ':' + PORT + '/' + 'Server/' + __setting__

execute_cmd = 'python ' + __mainfile__
execute_cmd_background = execute_cmd + ' &'
check_output_cmd = 'python -c "from ' + __mainfile__[:-3] + ' import __version__; print __version__"'

PIDKILL = ''
__version__ = '0.0.1'
######################################################################################################


def client_get_csv():
    print "Downloading file " + __configuration__ + "..."
    r = urlopen(csv_get_url, proxies=None)
    with open(__configuration__, 'wb') as fd:
        fd.write(r.read())


def client_get_main_file():
    print "Downloading file " + __mainfile__ + "..."
    r = urlopen(main_file_get_url, proxies=None)
    with open(__mainfile__, 'wb') as fd:
        fd.write(r.read())


def client_get_setting():
    print "Downloading file " + __setting__ + "..."
    r = urlopen(setting_get_url, proxies=None)
    with open(__setting__, 'wb') as fd:
        fd.write(r.read())


def client_get_mainfile_version():
    '''
        This function reads the first line of the main file and parse the version,
        therefore the first line should end with file version, somehing like:
        __version__ = '0.0.1'
    '''
    r = urlopen(main_file_get_url, proxies=None)
    version = r.readline()[-7:-2]
    return version


def client_get_setup_version():
    r = urlopen(setting_get_url, proxies=None)
    version = r.readline().strip()  # strip the first row
    return version


def get_pid():
    '''
        This function aimed to get the pid of the executing command
        (the number '5724' in the bellow example)

        ubuntu@1605I0000033$ ps -ef |grep Toy.py
        ubuntu     5724  6364  0 09:08 pts/4    00:00:00 python Toy.py
        ubuntu     5725  6347  0 09:09 pts/3    00:00:00 grep --color=auto Toy.py

    '''
    fetch_pid = 'ps -ef |grep ' + __mainfile__
    program_list = check_output(fetch_pid, shell=True).split("\n")
    for list in program_list:
        if list[-len(execute_cmd):] == execute_cmd:
            pid_list = list.split(' ')
    pID = [x for x in pid_list if x][1]
    KILL = 'kill ' + pID
    return KILL
    print "Terminating program ", __mainfile__, "-[", pID, "]"


def read_config_csv():
    f = open(__configuration__, "r")
    data = [x.strip() for x in f.readlines()]
    f.close()
    return (data)


def read_setting_csv():
    f = open(__setting__, "r")
    data = [x.strip() for x in f.readlines()]
    f.close()
    return (data)


if __name__ == '__main__':
    client_get_csv()
    client_get_setting()
    client_get_main_file()
    os.system(execute_cmd_background)  # start background program
    PIDKILL = get_pid()
    __version__ = check_output(check_output_cmd, shell=True)
    print "Current version is", __version__, "\n"
    while 1:
        try:
            client_get_csv()
            Update_list = read_config_csv()
            Setting_list = read_setting_csv()
            print "Setting_list", Setting_list
            print "Update_list: ", Update_list, "Current running version :", __version__
            if StrictVersion(Update_list[0]) > StrictVersion(__version__) and StrictVersion(Update_list[0]) == StrictVersion(client_get_mainfile_version()):
                os.system(PIDKILL)
                client_get_main_file()
                __version__ = check_output(check_output_cmd, shell=True)
                print "<===== RESTART ", __mainfile__, " version ", __version__[:-1], " =====>\n"
                os.system(execute_cmd_background)
                PIDKILL = get_pid()

            if StrictVersion(Update_list[1]) > StrictVersion(Setting_list[0]) and StrictVersion(Update_list[1]) == StrictVersion(client_get_setup_version()):
                client_get_setting()
                print "<===== RESTART ", __setting__, " version ", Setting_list[0], " =====>\n"
            time.sleep(5)

        except KeyboardInterrupt:
            os.system(PIDKILL)
            print "\n KeyboardInterrupt => Kill", __mainfile__, "--pid ", PIDKILL[6:]
            break

        except IOError as e:
            os.system(PIDKILL)
            print "IOError, Shutting down Update...\n", e
            break

        except Exception as e:
            os.system(PIDKILL)
            print "\n Shutting down Update..."
            print "======== Original error message ========"
            print e
            print "========================================"
            break
