#! /usr/local/bin/python

# Yuichi Shiraishi 2015/03/05
# script for extracting overlapping short reads

import sys, re 
inputFile = sys.argv[1]
mapQ = sys.argv[2]
overlapDist = int(sys.argv[3])

memDist = overlapDist 

inFile = open(inputFile, "r")
ID2row = {}
ID2chr = {}
ID2pos = {}

cigarRe = re.compile('^\d+M$')
for line in inFile:
    row = line.rstrip('\n')
    F = row.split('\t')

    # select properly aligned paired reads and non-supplementary and non-duplicated
    flags = format(int(F[1]), '#014b')[:1:-1]
    if flags[0] == 0 or flags[1] == 0 or flags[2] == 1 or flags[3] == 1 or flags[8] == 1 or flags[10] == 1 or flags[11] == 1:
        continue

    # skip the read with mapping quality below the specified value
    if F[4] < mapQ:
        continue

    # skip the read having some indels or soft clipping
    if cigarRe.match(F[5]) is None:
        continue

    delIDList = []
    matchFlag = 0
    for ID in ID2row:
        if ID2chr[ID] != F[2] or ID2pos[ID] < int(F[3]) - memDist:
            delIDList.append(ID)
        elif ID == F[0] and ID2pos[ID] >= int(F[3]) - overlapDist:
            print ID2row[ID]
            print row
            delIDList.append(ID)
            matchFlag = 1

    for ID in delIDList:
        del ID2row[ID]
        del ID2chr[ID]
        del ID2pos[ID]

    if matchFlag == 0: 
        ID2row[F[0]] = row
        ID2chr[F[0]] = F[2]
        ID2pos[F[0]] = int(F[3])

inFile.close()
