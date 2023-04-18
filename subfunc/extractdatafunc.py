import csv

def extractFileCol(file, col, divtype):
    l_data = []
    for row in csv.reader(open(file, 'r'), delimiter=divtype):
        l_data.append(row[col])

    return l_data

def extractFile2DCol(file, key, keycol, valuecol, divtype):
    for row in csv.reader(open(file, 'r'), delimiter=divtype):
        if row[keycol] == key:
            value = row[valuecol]

    return value
