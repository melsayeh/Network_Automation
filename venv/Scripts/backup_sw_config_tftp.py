from netmiko import ConnectHandler
from netmiko.ssh_exception import  NetMikoTimeoutException
from netmiko.ssh_exception import  AuthenticationException
from paramiko.ssh_exception import SSHException
from operator import itemgetter
import ntc_templates
from operator import itemgetter
import getpass
import time
import openpyxl
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
import netaddr
from netaddr import EUI
import ttp
import json
import csv
import logging
import alive_progress
from alive_progress import alive_bar

def getUsername():
    sshUsername = input("Enter SSH username: ")
    return(sshUsername)

### GET PASSWORD AS USER INPUT
def getPassword():
    pwd = getpass.getpass(prompt='Enter SSH password: ')
    return(pwd)

#### CALL FUNCTIONS
username = getUsername()
password = getPassword()

#### DEFINE SWITCH VENDOR
plateform = 'hp_procurve'


##### OPEN AND READ SWITCH IP FROM A LIST
switches = open('/home/switches/ip_list', 'r')

with alive_bar(15) as bar:
    for host in switches.readlines():   ##### LOOP THROUGH A LIST OF MULTIPLE SWITCHES ###########
        host = host.strip()
        switch_ip = host.strip('\n')
        while True:
            try:
                print(host)
                ######### ESTABLISH SSH CONNECTION TO THE SWITCH ############
                net_connect = ConnectHandler(device_type=plateform, ip=host, username=username, password=password)
                n=1
                print(50 * '*' + "\nConnecting to " + host.strip('\n') + ". Please wait ..." + "\n\n")

                command = 'copy running-config tftp 10.109.103.129 ' + host + '.txt'

                output = net_connect.send_command(command)
                print(output)
                logging.basicConfig(filename='/home/switches/debug.log', level=logging.DEBUG)
                logger = logging.getLogger("netmiko")



            except (AuthenticationException):
                print('Authentication Failure. Please try again:\n')
                username = getUsername()
                password = getPassword()
                continue

            except (NetMikoTimeoutException):
                print('Connection Timeout. Reconnecting ...')
                time.sleep(5)
                n+=1
                if(n<4):
                    print('Unable to establish a connection to: ', host)
                    continue
                else: pass
            break
        bar()