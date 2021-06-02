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
import re
import pandas


def getUsername():
    sshUsername = input("Enter SSH username: ")
    return(sshUsername)

def getPassword():
    pwd = getpass.getpass(prompt='Enter SSH password: ')
    return(pwd)


username = getUsername()
password = getPassword()
plateform = 'cisco_ios'
switches = open('/home/switches/ip_list.txt', 'r')
command_list = open('/home/switches/dot1x.txt')
dot1x = [line.rstrip() for line in command_list]
with open('/home/switches/switch_interfaces_down.csv','w') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ', quotechar='|')
    fields = ['switch_ip', 'interfaces', 'name', 'vlan', 'status']
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    for host in switches:
        host = host.strip()
        while True:
            try:
                net_connect = ConnectHandler(device_type=plateform, ip=host, username=username, password=password, session_log='/home/switches/output.log')
                n=1
                print(50 * '*' + "\nConnecting to " + host.strip('\n') + ". Please wait ..." + "\n\n")

                #get the output of the command #show interface brief
                switchX = net_connect.send_command("show interface status", use_textfsm=True)

                #set ntc_templates item getters
                getintname = itemgetter('name')
                getstatus = itemgetter('status')
                getinterfaces = itemgetter('port')
                getvlan = itemgetter('vlan')


                switch_ip = host.strip('\n')
                port_list = []

                #parse through the output and fetch data using the item getters
                for i in switchX:
                    interface = getinterfaces(i).strip('\n')
                    intname = getintname(i)
                    status = getstatus(i)
                    vlan = getvlan(i)

                    #set the conditions to filter out particular interfaces
                    regex1 = re.compile('^Po*')
                    regex2 = re.compile('^Te*')
                    regex3 = re.compile('^Gi.\/1\/.')
                    if status=='notconnect' and vlan != '101' and not regex1.match(interface) and not regex2.match(interface) and not regex3.match(interface):
                        writer.writerow({'switch_ip': switch_ip, 'interfaces': interface, 'name': intname, 'vlan': vlan,
                                     'status': status})
                        port_list.append(interface)



                #divide the port_list into groups of 4 for the command #interface range# limitation
                n=8
                f = ""
                list_of_groups = [port_list[i:i + n] for i in range(0, len(port_list), n)]

                #configure the list of interfaces
                output2 = net_connect.send_command_timing("configure terminal", cmd_verify=False)
                print(output2)
                for i in list_of_groups:
                    f=" , ".join(i)
                    command = "interface range "+ f
                    #print(command)
                    output3 = net_connect.send_command_timing(command, cmd_verify=False)
                    print(output3)
                    output4 = net_connect.send_config_set(dot1x, cmd_verify=False, exit_config_mode=False)
                    print(output4)
                    output5 = net_connect.send_command_timing("do write memory", cmd_verify=False)

                print("\nConfig has been pushed successfully!\n" + 50 * '*')
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