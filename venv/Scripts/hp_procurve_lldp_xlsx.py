from netmiko import ConnectHandler
from netmiko.ssh_exception import  NetMikoTimeoutException
from netmiko.ssh_exception import  AuthenticationException
from paramiko.ssh_exception import SSHException
from operator import itemgetter
import ntc_templates
from operator import itemgetter
import getpass
import time
import openpyxl
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
import netaddr
from netaddr import EUI
import ttp
import json
import csv

### GET USERNAME AS USER INPUT
def getUsername():
    sshUsername = input("Enter SSH username: ")
    return(sshUsername)

### GET PASSWORD AS USER INPUT
def getPassword():
    pwd = getpass.getpass(prompt='Enter SSH password: ')
    return(pwd)

#### CONVERT MAC ADDRESS TO UNIX FORMAT
def convertMac2Unix(octet):
    new_mac = ''
    if octet != None:
        if octet[2] == ':' :
            new_mac = octet.replace( ':' ,'' )
        elif octet[2] == '.' or octet[4] == '.' or octet[5] == '.':
            new_mac = octet.replace( '.' , '' )
        elif octet[2] == '-' or octet[6] == '-' :
            new_mac = octet.replace( '-' , '' )
        else: pass
    x=0
    result = ''
    for letter in new_mac:
        if x != 0 and x % 2 == 0 :
            result += ':'
            result += letter
        else:
            result += letter
        x+=1

    return(result)


#### CALL FUNCTIONS
username = getUsername()
password = getPassword()

#### DEFINE SWITCH VENDOR
plateform = 'hp_procurve'


##### OPEN AND READ SWITCH IP FROM A LIST
switches = open('/home/switches/ip_list', 'r')


######### CREATE A NEW XLSX WORKBOOK
wb = Workbook()
dst_filename = '/home/switches/test.xlsx'
wb.save(dst_filename)
ws1 = wb.active
ws1.title = "LLDP_INFO"
ws1.append(["Switch IP", "Port Number", "Remote Device IP", "Remote Device Name", "Remote Device MAC", "Remote Device Model"])
ws2 = wb.create_sheet("SWITCH_INFO")
ws2.append(["Switch IP", "Name", "MAC Address", "Software Ver", "Serial"])
ws3 = wb.create_sheet("Final_WB")
ws3.append(["Switch IP", "Port#", "Port Number", "Link Location", "Native/Untagged VLAN", "Allowed/Tagged VLAN", "Virtual Port", "Punch Panel", "Description", "State"])


for host in switches.readlines():   ##### LOOP THROUGH A LIST OF MULTIPLE SWITCHES ###########
    host = host.strip()
    switch_ip = host.strip('\n')
    while True:
        try:
            print(host)
            ######### ESTABLISH SSH CONNECTION TO THE SWITCH ############
            net_connect = ConnectHandler(device_type=plateform, ip=host, username=username, password=password)
            n=1
            print(50 * '*' + "\nConnecting to " + host.strip('\n') + ". Please wait ..." + "\n\n")
            output = net_connect.send_command("show lldp info remote detail", use_textfsm=True) #Collect LLDP details
            print("****** Fetching LLDP data from", host.strip('\n'), " ********")
            output2 = net_connect.send_command("show system", use_textfsm=True) #Collect switch info
            print("****** Fetchine switch info from", switch_ip, " ********")
            output3 = net_connect.send_command("show run interface", use_ttp=True, ttp_template="show_run_int.ttp") #Collect interfaces details
            output4 = net_connect.send_command("show interfaces brief", use_ttp=True, ttp_template="show_int_br.ttp")
            l=0

            for line in output:
                switchX = output[l]
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

                ws1.append([switch_ip, port_number, nei_ip, nei_name, convertMac2Unix(nei_mac), nei_model])

                l+=1
            wb.save(dst_filename)


            x = 0
            for lines in output2:
                switchXX = output2[x]

                ########## SET ITEM GETTERS ##############
                getname = itemgetter('name')
                getmac = itemgetter('mac')
                getver = itemgetter('software_version')
                getserial = itemgetter('serial')

                ########### USE ITEM GETTERS TO FETCH DATA FROM THE STRUCTURED OUTPUT ###########
                switch_name = getname(switchXX)
                switch_mac = getmac(switchXX)
                switch_ver = getver(switchXX)
                switch_serial = getserial(switchXX)

                if switch_mac != "":
                    ws2.append([switch_ip, switch_name, convertMac2Unix(switch_mac), switch_ver, switch_serial])
                else:
                    ws2.append([switch_ip, switch_name, switch_mac, switch_ver, switch_serial])

                x += 1
            wb.save(dst_filename)


            for f in output3[0]:

                if f == output3[0][0]: continue ## This is to skip first row (table header)
                else:
                    if len(f)==3:

                        ws3.append([switch_ip, f[0], None, f[2], f[1]])
                    else:
                        ws3.append([switch_ip, f[1], None, f[3], f[2]])

            k=0
            for row in ws3.iter_rows():
                final_swIP = ws3.cell(row=k + 1, column=1)
                final_port = ws3.cell(row=k + 1, column=2)
                final_linklocation = ws3.cell(row=k + 1, column=3)
                final_desc = ws3.cell(row=k + 1, column=8)

                k+=1
                j = 0
                for ll in ws1.iter_rows():
                    lldp_port = ws1.cell(row=j + 1, column=2)
                    hostip = ws1.cell(row=j + 1, column=1)
                    lldp_name = ws1.cell(row=j + 1, column=4)
                    lldp_mac = ws1.cell(row=j + 1, column=5)

                    j+=1
                    if final_swIP.value == hostip.value and final_port.value == lldp_port.value:
                        final_linklocation.value = lldp_mac.value
                        final_desc.value = lldp_name.value
                    else: continue




            wb.save(dst_filename)
            print("\nData has been extracted successfully!\n" + 50 * '*' + '\n')
            net_connect.disconnect()



        except (AuthenticationException):
            print('Authentication Failure. Please try again:\n')
            username = getUsername()
            password = getPassword()
            continue

        except (NetMikoTimeoutException):
            print('Connection Timeout. Reconnecting ...')
            time.sleep(5)
            n+=1
            if(n<4):
                continue
            else: pass
        break