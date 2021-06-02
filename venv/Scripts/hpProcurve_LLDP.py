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
import openpyxl


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
with open('/home/switches/switch_lldp.csv','w') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ', quotechar=';')
    fields = ['switch_ip', 'port_number', 'nei_ip', 'nei_name' , 'nei_mac' , 'nei_model']
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    for host in switches:   ##### LOOP AROUND A LIST OF MULTIPLE SWITCHES ###########
        host = host.strip()
        while True:
            try:
                ######### ESTABLISH SSH CONNECTION TO THE SWITCH ############
                net_connect = ConnectHandler(device_type=plateform, ip=host, username=username, password=password)
                n=1
                print(50 * '*' + "\nConnecting to " + host.strip('\n') + ". Please wait ..." + "\n\n")
                output = net_connect.send_command("show lldp info remote detail", use_textfsm=True)
                l=0
                for line in output:
                    switchX = output[l]
                    print(switchX)
                    switch_ip = host.strip('\n')

                    ########## SET ITEM GETTERS ##############
                    getportnumber = itemgetter('local_port')
                    getneiip = itemgetter('remote_management_address')
                    getneiname = itemgetter('neighbor_sysname')
                    getneimac = itemgetter('neighbor_chassis_id')
                    getneimodel = itemgetter('system_descr')

                    ########### USE ITEM GETTERS TO FETCH DATA FROM THE STRUCTURED OUTPUT ###########
                    port_number = getportnumber(switchX)
                    nei_ip = getneiip(switchX)
                    nei_name = getneiname(switchX)
                    nei_mac = getneimac(switchX)
                    nei_model = getneimodel(switchX)

                    ########### WRITE FETCHED DATA INTO THE CSV FILE ############
                    writer.writerow({'switch_ip': switch_ip, 'port_number': port_number, 'nei_ip': nei_ip, 'nei_name': nei_name, 'nei_mac': nei_mac, 'nei_model': nei_model})
                    print(switch_ip + ' ' + port_number + ' ' + nei_ip + ' ' + nei_name)
                    l+=1

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
                if(n<3):
                    continue
                else: break

            break

