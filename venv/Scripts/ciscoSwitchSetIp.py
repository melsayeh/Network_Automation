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
plateform = 'cisco_ios'
switches = open('/home/switches/ip_list', 'r')
x=12
for host in switches:
    host = host.strip()
    while True:
        try:
            n=1
            net_connect = ConnectHandler(device_type=plateform, ip=host, username=username, password=password, global_delay_factor=5, ssh_config_file='~/.ssh/config')
            print (net_connect.find_prompt())
            net_connect.write_channel('command to access switch')
            time.sleep(1)
            net_connect.read_channel()
            redispatch(net_connect, device_type=cisco_ios)

            print(50 * '*' + "\nConnecting to " + host.strip('\n') + ". Please wait ..." + "\n\n")
            output0 = net_connect.send_command_timing("configure terminal")
            print(output0)
            output1 = net_connect.send_command_timing("ip default-gateway 10.248.243.2")
            print(output1)
            output2 = net_connect.send_command_timing("no ntp server 10.1.100.1")
            print(output2)
            output3 = net_connect.send_command_timing("ntp server 10.248.243.2")
            print(output3)
            output5 = net_connect.send_command_timing("do write memory")
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

