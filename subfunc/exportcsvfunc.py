import csv
import os

def exportCSVFile(filename, data):
    is_file = os.path.isfile(filename)
    if is_file:
        addDataCSVFile(filename, data)
    else:
        createNewCSVFile(filename, data)

def addDataCSVFile(filename, data):
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def createNewCSVFile(filename, data):
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(data)
