import csv

def extractTsvCol(file, col):
    l_data = []
    for row in csv.reader(open(file, 'r'), delimiter='\t'):
        l_data.append(row[col])

    return l_data

