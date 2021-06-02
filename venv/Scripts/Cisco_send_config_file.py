from netmiko import ConnectHandler
from netmiko.ssh_exception import  NetMikoTimeoutException
from netmiko.ssh_exception import  AuthenticationException
from paramiko.ssh_exception import SSHException
from operator import itemgetter
import ntc_templates
import os
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
plateform = 'cisco_ios'
switches = open('D:/Python/Cisco_add_username/ip_list.txt', 'r')
config_file = open('D:\OneDrive - Guest-Tek\OneDrive - Guest-Tek Interactive Entertainment Ltd\Projects\Installation Guides\Switches\Cisco_Catalyst_basic_gtk_gpns.txt')
#config_content = config_file.readline()
command_list = [line.rstrip() for line in config_file]
x=12
n = 1
for host in switches:
    host = host.strip()
    while True:
        try:
            #print(command_list)
            net_connect = ConnectHandler(device_type=plateform, ip=host, username=username, password=password, global_delay_factor=5, session_log='output.log')
            print (net_connect.find_prompt())
            net_connect.write_channel('command to access switch')
            time.sleep(1)
            net_connect.read_channel()
            redispatch(net_connect, device_type='cisco_ios')

            print(50 * '*' + "\nConnecting to " + host.strip('\n') + ". Please wait ..." + "\n\n")
            output0 = net_connect.send_config_set(command_list, cmd_verify=False)
            print(output0)
            print("\nConfiguration has been pushed successfully!\n" + 50 * '*')
            net_connect.disconnect()


        except (AuthenticationException):
            print(username + '/' + password)
            print('Authentication Failure. Please try again:\n')
            username = getUsername()
            password = getPassword()
            continue


        except (NetMikoTimeoutException):
            print('Connection Timeout. Reconnecting ...')
            time.sleep(10)
            n+=1
            if(n<4):
                continue
            else: pass

        break

