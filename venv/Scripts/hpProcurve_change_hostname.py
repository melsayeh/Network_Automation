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
hostnames = open('/home/switches/hostnames', 'r')
x=12
for host,hostname in zip(switches,hostnames):
    host = host.strip()
    hostname = hostname.strip()
    while True:
        try:
            n=1
            net_connect = ConnectHandler(device_type=plateform, ip=host, username=username, password=password)

            print(50 * '*' + "\nConnecting to " + host.strip('\n') + ". Please wait ..." + "\n\n")
            output0 = net_connect.send_command_timing("configure terminal")
            print(output0)
            command1 = "hostname "+ hostname
            output1 = net_connect.send_command_timing(command1)
            print(output1)
            output5 = net_connect.send_command_timing("write memory")
            print(output5)
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
            if(n<4):
                continue
            else: pass

        break

