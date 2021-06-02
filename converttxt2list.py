import csv
idiomsFile = open("idioms.txt", "r", encoding="UTF-8")
idiomList = []
desc = ""
descList = []
i = 0
x = 0
for line in idiomsFile.readlines():
    if line[0].isnumeric():
        idiomList.append(line)
idiomsFile.close()

idiomsFile = open("idioms.txt", "r", encoding="UTF-8")
for line in idiomsFile.readlines():
    if not line[0].isnumeric():
        desc += line
    else:
        descList.append(desc)
        desc = ""
del (descList[0])
idiomsFile.close()

idiomDic = list(zip(idiomList, descList))

with open("idiomCsv.csv", "w") as save:
    writer = csv.writer(save)
    writer.writerows(idiomDic)

save.close()
