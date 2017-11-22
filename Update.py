#!/usr/bin/env python

import csv
import os
import time
from distutils.version import StrictVersion
from subprocess import check_output
from urllib import urlopen

############# Initial Setting ############
MAC = '10.137.99.200'                    #
#MAC = '192.168.0.110'                   #
__configuration__ = 'config.csv'         #
__mainfile__ = 'Toy.py'                  #
__setting__ = 'Toy_setting.csv'          # 
__version__ = '0.0.1'                    #
##########################################

csv_get_url = 'http://'+MAC+':8000/Server/'+__configuration__
main_file_get_url = 'http://'+MAC+':8000/Server/'+__mainfile__
setting_get_url = 'http://'+MAC+':8000/Server/'+__setting__

execute_cmd = 'python ' + __mainfile__
execute_cmd_background = execute_cmd + ' &'
check_output_cmd = 'python -c "from '+__mainfile__[:-3]+' import __version__; print __version__"'
PIDKILL = ''
__version__ = '0.0.0'
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

def restart_background_program():
    os.system(execute_cmd_background)

def find_program(program_list):
    for list in program_list:
        if list[-len(execute_cmd):] == execute_cmd:
            return list

def get_pid():
    '''
        In this function we want to get the pid of the executing command
        (the number"5724" in the bellow example)
        
        ubuntu@1605I0000033:$ ps -ef |grep Toy.py
        ubuntu     5724  6364  0 09:08 pts/4    00:00:00 python Toy.py
        ubuntu     5725  6347  0 09:09 pts/3    00:00:00 grep --color=auto Toy.py
    '''
    fetch_pid = 'ps -ef |grep '+ __mainfile__
    program_list = check_output(fetch_pid, shell=True).split("\n")
    for list in program_list:
        if list[-len(execute_cmd):] == execute_cmd:
            pid_list= list.split(' ')
    pID = [x for x in pid_list if x][1]
    KILL = 'kill '+ pID
    return KILL
    print "Terminating program ",__mainfile__,"-[",pID,"]"

def read_config_csv():
    f = open(__configuration__, "r")
    data = [x.strip() for x in f.readlines()]
    f.close()
    return (data)

def write_config_csv(data):
    f = open(__configuration__, "w")
    for string in data:
        f.writelines(string + '\n')
    f.close()

def read_setting_csv():
    f = open(__setting__, "r")
    data = [x.strip() for x in f.readlines()]
    f.close()
    return (data)

if __name__ == '__main__':
    client_get_csv()
    client_get_setting()
    client_get_main_file()
    restart_background_program()
    PIDKILL = get_pid()
    __version__ = check_output(check_output_cmd,shell = True)
    print "Current version is", __version__
    print "\n"
    while(1):
        try:
            client_get_csv()
            Update_list = read_config_csv()
            Setting_list = read_setting_csv()
            print "Setting_list",Setting_list
            print "Update_list: ",Update_list, "Current running version :",__version__
            if StrictVersion(Update_list[0]) > StrictVersion(__version__):
                os.system(PIDKILL)
                client_get_main_file()
                __version__ = check_output(check_output_cmd,shell = True)
                print "<===== RESTART ",__mainfile__," version ", __version__[:-1]," =====>"
                print "\n"
                restart_background_program()
                PIDKILL = get_pid()

            if StrictVersion(Update_list[1]) > StrictVersion(Setting_list[0]):
                client_get_setting()
                print "<===== RESTART ",__setting__," version ", Setting_list[0]," =====>"
                print "\n"
            
            time.sleep(25)
        except KeyboardInterrupt:
            os.system(PIDKILL)
            print "\n KeyboardInterrupt => Kill",__mainfile__,"--pid ",PIDKILL[6:]
            break
        except:
            print "Error. Terminating Upating system"
            break