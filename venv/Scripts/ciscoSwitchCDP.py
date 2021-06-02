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
from ntc_templates import

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
with open('/home/switches/switch_cdp.csv','w') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ', quotechar='|')
    fields = ['switch_ip', 'port_number', 'nei_ip', 'nei_name']
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    for host in switches:
        host = host.strip()
        while True:
            try:
                net_connect = ConnectHandler(device_type=plateform, ip=host, username=username, password=password)
                n=1
                print(50 * '*' + "\nConnecting to " + host.strip('\n') + ". Please wait ..." + "\n\n")
                output = net_connect.send_command("show cdp neighbor detail", use_textfsm=True)
                switchX = output[0]
                print(switchX)
                getportnumber = itemgetter('local_port')
                getneiip = itemgetter('management_ip')
                getneiname = itemgetter('destination_host')

                switch_ip = host.strip('\n')
                port_number = getportnumber(switchX)
                nei_ip = getneiip(switchX)
                nei_name = getneiname(switchX)


                writer.writerow({'switch_ip': switch_ip, 'port_number': port_number, 'nei_ip': nei_ip, 'nei_name': nei_name})
                print(switch_ip + ' ' + port_number + ' ' + nei_ip + ' ' + nei_name)

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

