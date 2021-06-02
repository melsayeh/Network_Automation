#!/usr/bin/env python
from netmiko import ConnectHandler
from getpass import getpass
from pprint import pprint
from ttp import ttp
import csv

ip_list= open('/home/switches/ip_list.txt', 'r')

command = "show interface status"
username = input("Enter Username: ")
password = getpass()
plateform = 'cisco_ios'


for host in ip_list:
    host = host.strip()
    print('*'*50)
    print(f'Please hold on while the script is checking ' + host + ' do not alt the script.')
    device = ConnectHandler(device_type=plateform, ip=host, username=username, password=password)
    output = device.send_command("show interfaces status")
    parser = ttp(data = output , template = "/home/switches/show_interface_status.ttp")
    parser.parse()
    result = parser.result(format="csv")

    print(result[0])


print('*'*50)
print('Export complete, please check the Output folder.')

#Single connection command
##############################
# print()
# pprint(output)
# print()
##############################
