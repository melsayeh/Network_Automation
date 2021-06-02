import ttp
import os

from ttp import ttp
parser = ttp(data="D:/Python/Export AP info from Cisco WLC 5760/AP_raw_data.txt", template="D:/Python/Export AP info from Cisco WLC 5760/ttp_template.txt")
parser.parse()
result = parser.result(format="csv")
print(result[0])




