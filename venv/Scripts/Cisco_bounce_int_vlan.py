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
import os
import re


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
with open('D:/Python/Cisco_add_username/switch_vlan_interfaces.csv','w') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ', quotechar='|')
    fields = ['switch_ip', 'vlan_id', 'interfaces']
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    for host in switches:
        host = host.strip()
        while True:
            try:
                net_connect = ConnectHandler(device_type=plateform, ip=host, username=username, password=password)
                n=1
                print(50 * '*' + "\nConnecting to " + host.strip('\n') + ". Please wait ..." + "\n\n")
                output = net_connect.send_command("show vlan id 652", use_textfsm=True)
                switchX = output[0]
                #print(switchX)
                getvlanid = itemgetter('vlan_id')
                getinterfaces = []
                getinterfaces = itemgetter('interfaces')

                switch_ip = host.strip('\n')
                interfaces = getinterfaces(switchX)
                vlan_id = getvlanid(switchX)

                regex1 = re.compile('^Po*')
                regex2 = re.compile('^Te*')
                filtered_interfaces = [x for x in interfaces if not regex1.match(x) or regex2.match(x)]
                print(filtered_interfaces)

                output2 = net_connect.send_command_timing("configure terminal", cmd_verify=False)
                print(output2)
                for p in filtered_interfaces:
                    command = "interface "+ str(p)
                    print(command)
                    output3 = net_connect.send_command_timing(command, cmd_verify=False)
                    print(output3)
                    output4 = net_connect.send_command_timing("shutdown", cmd_verify=False)
                    print(output4)
                    time.sleep(2)
                    output5 = net_connect.send_command_timing("no shut", cmd_verify=False)
                    print(output5)

                writer.writerow({'switch_ip': switch_ip, 'vlan_id': vlan_id, 'interfaces': filtered_interfaces})
                #print(switch_ip + ' ' + vlan_id + ' ' + str(filtered_interfaces))

                print("\nData has been extracted successfully!\n" + 50 * '*')
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