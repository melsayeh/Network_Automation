readFile = open("file.txt", "r")
fileContent = readFile.readlines()
for line in fileContent:
    print(line)
readFile.close()
