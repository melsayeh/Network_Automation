import json
from collections import OrderedDict
from openpyxl import load_workbook
import meraki
import os

#Authentication
API_KEY = '779d718249a9dd57c64529bd2b00b4872c0cdb95'
dashboard = meraki.DashboardAPI(API_KEY)

# Open the workbook and select a worksheet
# The file header must follow this order: IDF#, Switch_Seq, Switch_SN, Port#, Port_Name, Port_Mode, VLAN_ID, NATIVE_VLAN, ALLOWED_VLANS, Port_Isolation
wb = load_workbook('D:/OneDrive - Guest-Tek/OneDrive - Guest-Tek Interactive Entertainment Ltd/Projects/BAHTA/PythonScript.xlsx')
sheet = wb['Sheet3']
row_count = sheet.max_row

#Iterate through the excel sheet
for i in range (row_count):

    #Read a row and extract config params
    switch_sn = sheet.cell(row=i+1, column=2).value
    switch_name = sheet.cell(row=i+1, column=3).value
    networkId = 'L_708753991357433638'
    lan_ip = sheet.cell(row=i+1, column=4).value
    subnet_mask = '255.255.252.0'
    vlan_id = '700'
    gateway_ip = '192.168.0.1'
    primary_dns = '1.1.1.1'
    secondary_dns = '1.0.0.1'


    #Skip the 1st row - sheet header
    if i==0:
        continue

    response = dashboard.devices.updateDevice(
        network_id = networkId,
        serial = switch_sn,
        name=switch_name,
        vlan = vlan_id,
        lanIp = lan_ip,
        subnetMask = subnet_mask,
        gatewayIp = gateway_ip,
        primaryDns = primary_dns,
        secondaryDns = secondary_dns
    )
    print(response)
