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
model = []
serial = []
mac = []
with open('/home/switches/switch_inventory.csv','w') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ', quotechar='|')
    fields = ['hostIP', 'hostname', 'serial', 'mac_address', 'model', 'version']
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    for host in switches:
        host = host.strip()
        while True:
            try:
                net_connect = ConnectHandler(device_type=plateform, ip=host, username=username, password=password)
                n=1
                print(50 * '*' + "\nConnecting to " + host.strip('\n') + ". Please wait ..." + "\n\n")
                output = net_connect.send_command("show version", use_textfsm=True)
                switchX = output[0]
                gethostname = itemgetter('hostname')
                getversion = itemgetter('version')
                getmodel = itemgetter('hardware')
                getserial = itemgetter('serial')
                getmac = itemgetter('mac')

                hostIP = host.strip('\n')
                hostname = gethostname(switchX)
                version = getversion(switchX)
                model = getmodel(switchX)
                serial = getserial(switchX)
                mac = getmac(switchX)
                print(len(model))

                i = 0
                for record in model:
                    writer.writerow({'hostIP': hostIP, 'hostname': hostname, 'serial': serial[i], 'mac_address': mac[i],
                                     'model': model[i], 'version': version})
                    print(hostIP + ' ' + hostname + ' ' + serial[i] + ' ' + mac[i] + ' ' + model[i] + ' ' + version)
                    i = i + 1

                print("\nData has been extracted successfully!\n" + 50 * '*')
                net_connect.disconnect()


            except (AuthenticationException):
                print(username + '/' + password)
                print('Authentication Failure. Please try again:\n')
                username = getUsername()
                password = getPassword()
                continue

            except (NetMikoTimeoutException):
                n=1
                print('Connection Timeout. Reconnecting ...')
                time.sleep(10)
                if(n<3):
                    continue
                    n=n+1
                else: break

            break

