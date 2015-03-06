#! /usr/local/bin/python

import sys 
inputFile = sys.argv[1]
window = int(sys.argv[2])

inFile = open(inputFile, "r")
for line in inFile:
    F = line.rstrip('\n').split('\t')
    print F[1] + "\t" + str(max(1, int(F[2]) - window)) + "\t" + str(int(F[3]) + window)

inFile.close()
