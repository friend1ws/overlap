#! /usr/local/bin/python

import sys
inputFile = sys.argv[1]

inFile = open(inputFile, 'r')
for line in inFile:
    F = line.rstrip('\n').split('\t')
    if F[11] == "single":
        print F[1] + '\t' + F[2] + '\t' + F[3] + '\t' + F[4]

inFile.close()

