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
x=12
n = 1
for host in switches:
    host = host.strip()
    while True:
        try:
            net_connect = ConnectHandler(device_type=plateform, ip=host, username=username, password=password)
            print(50 * '*' + "\nConnecting to " + host.strip('\n') + ". Please wait ..." + "\n\n")
            output0 = net_connect.send_command_timing("configure terminal")
            print(output0)
            output1 = net_connect.send_command_timing("file prompt quiet")
            print(output1)
            output5 = net_connect.send_command_timing("exit")
            print(output5)
            command = "copy running-config tftp://10.248.243.1/"+host+".txt"
            output6 = net_connect.send_command_timing(command)
            print(output6)
            print("\nConfiguration has been pushed successfully!\n" + 50 * '*')
            net_connect.disconnect()


        except (AuthenticationException):
            print(username + '/' + password)
            print('Authentication Failure. Please try again:\n')
            username = getUsername()
            password = getPassword()


        except (NetMikoTimeoutException):
            print('Connection Timeout. Reconnecting ...')
            time.sleep(10)
            n+=1
            if(n<4):
                continue
            else: pass

        break

