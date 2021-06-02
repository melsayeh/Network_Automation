from typing import Dict

from netmiko import ConnectHandler
import getpass
import sys
import time

device: Dict[str, str] = {
    'device_type': 'hp_procurve',
    'ip': '192.168.43.10',
    'username': 'username',
    'password': 'password',
}
ipfile = open("/home/switches/ip_list")
#print("Script for SSH to device, Please enter your credential")
device['username'] = 'melsayeh'
device['password'] = 'Ma1ri2am'
configfile = open("/home/switches/configfile.txt")
configset = configfile.readline()
configfile.close()

#for line in ipfile:
#    device['ip'] = line.strip("\n")
device['ip'] = "10.251.223.152"
print("\n\nConnecting Device ", "10.251.223.152")
net_connect = ConnectHandler(**device)
net_connect.enable()
time.sleep(3)
print("Passing configuration set ")
net_connect.send_config_set(configset)
print("Device Configured ")
net_connect.disconnect()
ipfile.close()