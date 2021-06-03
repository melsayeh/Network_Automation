import json
from collections import OrderedDict
from openpyxl import load_workbook
import meraki
import os

#Authentication
API_KEY = 'API_KEY_HERE'
dashboard = meraki.DashboardAPI(API_KEY)

# Open the workbook and select a worksheet
# The file header must follow this order: IDF#, Switch_Seq, Switch_SN, Port#, Port_Name, Port_Mode, VLAN_ID, NATIVE_VLAN, ALLOWED_VLANS, Port_Isolation
wb = load_workbook('/PATH/TO/WORKBOOK')
sheet = wb['Sheet1']
row_count = sheet.max_row

#Iterate through the excel sheet
for i in range (row_count):

    #Read a row and extract config params
    switch_sn = sheet.cell(row=i+1, column=3).value
    port_no = sheet.cell(row=i+1, column=4).value
    port_name = sheet.cell(row=i+1, column=5).value
    port_mode = sheet.cell(row=i+1, column=6).value
    vlan_id = sheet.cell(row=i+1, column=7).value
    native_vlan = sheet.cell(row=i+1, column=8).value
    allowed_vlan = sheet.cell(row=i+1, column=9).value
    isolation = sheet.cell(row=i+1, column=10).value

    #Skip the 1st row - sheet header
    if i==0:
        continue

    #If the port is trunk, assign the native vlan and set allowed vlans
    if port_mode == "trunk":
        response = dashboard.switch.updateDeviceSwitchPort(
            serial= switch_sn,
            portId= port_no,
            name = port_name,
            type= port_mode,
            vlan= native_vlan,
            allowedVlans= allowed_vlan,
            isolationEnabled= isolation,
        )
    #Otherwise, configure the port as access
    else:
        response = dashboard.switch.updateDeviceSwitchPort(
            serial=switch_sn,
            portId=port_no,
            name=port_name,
            type=port_mode,
            vlan=vlan_id,
            isolationEnabled= isolation,

        )

    print(response)
