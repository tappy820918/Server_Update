#!/usr/bin/env python

import csv
import os
import time
from distutils.version import StrictVersion
from subprocess import check_output
from urllib import urlopen

############# Initial Setting ############
#MAC = '10.137.98.199'                   #
MAC = '192.168.0.107'                    #
csv_path = 'config.csv'                  #
main_file = 'Toy.py'                     #
__version__ = '0.0.1'                    #
##########################################

csv_get_url = 'http://'+MAC+':8000/Server/'+csv_path
main_file_get_url = 'http://'+MAC+':8000/Server/'+main_file
execute_cmd = 'python ' + main_file
execute_cmd_background = execute_cmd + ' &'
check_output_cmd = 'python -c "from '+main_file[:-3]+' import __version__; print __version__"'
PIDKILL = ''
__version__ = check_output(check_output_cmd,shell = True)
def client_get_csv():
    print "Downloading file " + csv_path + "..."
    r = urlopen(csv_get_url, proxies=None)
    with open(csv_path, 'wb') as fd:
        fd.write(r.read())

def client_get_main_file():
    print "Downloading file " + main_file + "..."
    r = urlopen(main_file_get_url, proxies=None)
    with open(main_file, 'wb') as fd:
        fd.write(r.read())

def restart_background_program():
    os.system(execute_cmd_background)

def find_program(program_list):
    for list in program_list:
        if list[-len(execute_cmd):] == execute_cmd:
            return list

def get_pid():
    fetch_pid = 'ps -ef |grep '+ main_file
    program_list = check_output(fetch_pid, shell=True).split("\n")
    for list in program_list:
        if list[-len(execute_cmd):] == execute_cmd:
            pid_list= list.split(' ')
    pID = [x for x in pid_list if x][1]
    KILL = 'kill '+ pID
    return KILL
    print "Terminating program ",main_file,"-[",pID,"]"

def read_config_csv():
    f = open(csv_path, "r")
    data = [x.strip() for x in f.readlines()]
    f.close()
    return (data)

def write_config_csv(data):
    f = open(csv_path, "w")
    for string in data:
        f.writelines(string + '\n')
    f.close()

if __name__ == '__main__':
    client_get_csv()
    client_get_main_file()
    restart_background_program()
    PIDKILL = get_pid()
    __version__ = check_output(check_output_cmd,shell = True)
    print "Current version is ", __version__
    while(1):
        try:
            client_get_csv()
            Update_list = read_config_csv()
            print "Update_list: ",Update_list, "Current running version :",__version__
            if StrictVersion(Update_list[0]) > StrictVersion(__version__):
                os.system(PIDKILL)
                client_get_main_file()
                __version__ = check_output(check_output_cmd,shell = True)
                print "<===== RESTART ",main_file," version ", __version__[:-1]," =====>"
                restart_background_program()
                PIDKILL = get_pid()
                
            time.sleep(5)
        except KeyboardInterrupt:
            os.system(PIDKILL)
            print "\n KeyboardInterrupt => Kill",main_file,"--pid ",PIDKILL[6:]
            break