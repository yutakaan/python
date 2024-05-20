import csv
import pandas as pd

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

def extractFile1KeyRowList(file, key1, keycol1, divtype):
    df_row = pd.DataFrame()
    for row in csv.reader(open(file, 'r'), delimiter=divtype):
        if row[keycol1] == key1:
            df_row = row

    return df_row

def extractFile2KeyRowList(file, key1, keycol1, key2, keycol2, divtype):
    df_row = pd.DataFrame()
    for row in csv.reader(open(file, 'r'), delimiter=divtype):
        if row[keycol1] == key1:
            if row[keycol2] == key2:
                df_row = row

    return df_row
