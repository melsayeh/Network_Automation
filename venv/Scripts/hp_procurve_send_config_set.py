from netmiko import ConnectHandler
from netmiko.ssh_exception import  NetMikoTimeoutException
from netmiko.ssh_exception import  AuthenticationException
from paramiko.ssh_exception import SSHException
from operator import itemgetter
import ntc_templates
from operator import itemgetter
import getpass
import csv
import time
from netmiko import redispatch


def getUsername():
    sshUsername = input("Enter SSH username: ")
    return(sshUsername)

def getPassword():
    pwd = getpass.getpass(prompt='Enter SSH password: ')
    return(pwd)

username = getUsername()
password = getPassword()
plateform = 'hp_procurve'
switches = open('/home/switches/ip_list', 'r')

configfile = open("/home/switches/configfile.txt")
configset = configfile.read()
configfile.close()

for host in switches:
    host = host.strip("\n")
    while True:
        try:
            n=1
            print(50 * '*' + "\nConnecting to " + host.strip('\n') + ". Please wait ..." + "\n\n")
            net_connect = ConnectHandler(device_type=plateform, ip=host, username=username, password=password, session_log="/home/switches/output.txt")
            #net_connect.enable()
            #time.sleep(5)
            print("Passing configuration set ")
            net_connect.send_config_set(configset, cmd_verify=False, exit_config_mode=False) #cmd_verify is to ignore prompt output   #exit_config_mode is to include the exit command within the config set file
            print("\nConfiguration has been pushed successfully!\n" + 50 * '*')
            net_connect.disconnect()
            #switches.close()

        except (AuthenticationException):
            print(username + '/' + password)
            print('Authentication Failure. Please try again:\n')
            username = getUsername()
            password = getPassword()
            continue

        except (NetMikoTimeoutException):
            print('Connection Timeout. Reconnecting ...')
            time.sleep(10)
            if(n<4):
                continue
            else: pass

        break