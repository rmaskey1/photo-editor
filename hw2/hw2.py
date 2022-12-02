import json

fileName = input("Enter file name: ")
tmp = fileName.rpartition(".")
fileNameLeft = tmp[0]
fileType = input("Type 'c' to save as csv file, 'j' to save as json file, and 'x' to save as xml file: ")

if fileType == "c":
    f = open(fileName, 'r')
    output = open(fileNameLeft + ".csv", 'w')
    data = f.read().replace('\t', ',')
    output.write(data)

elif fileType == "j":
    f = open(fileName, 'r')
    output = open(fileNameLeft + ".json", 'w')
    firstLine = f.readline()
    titles = firstLine.split("\t")

    for line in f:
        data = {}
        information = line.split("\t")
        i = 0
        for info in information:
            data[titles[i]] = info
            i += 1
        json.dump(data,output,indent=4)

elif fileType == "x":
    f = open(fileName, 'r')
    output = open(fileNameLeft + ".xml", 'w')
    firstline = f.readline()
    header = firstline.split('\t')
    output.write('<?xml version = "1.0" encoding="UTF-8"?>\n')
    output.write("<data>\n")
    lineNum = 1
    for line in f:
        information = line.split("\t")
        i = 0
        output.write("\t<row>\n")
        for info in information:
            headerinfo = header[i].replace(" ", "")
            headerinfo = headerinfo.replace("\n", "")
            infoInfo = information[i].replace("\n","")
            data = "\t\t"+"<"+headerinfo+">"+infoInfo+"</"+headerinfo+">\n"
            output.write(data)
            i += 1
        output.write("\t</row>\n")
        lineNum += 1
    output.write("</data>\n")
else:
    print("Invalid File Type")