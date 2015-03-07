#! /usr/local/bin/python

# checking the pileup data, remove the mismatch record breaking the specified depth and allele frequency condition

import sys

mismatchFile = sys.argv[1]
pileupFile = sys.argv[2]
depthMin = int(sys.argv[3])
depthMax = int(sys.argv[4])
AFMax = float(sys.argv[5])

filterPos = []
hPileupFile = open(pileupFile, 'r')
for line in hPileupFile:
    F = line.rstrip('\r').split('\t')

    if int(F[3]) < depthMin or int(F[3]) > depthMax:
        filterPos.append(F[0] + '\t' + F[1])
        continue
    
    matchNum1 = F[4].count('.')
    matchNum2 = F[4].count(',')
    misNum = int(F[3]) - matchNum1 - matchNum2

    if float(misNum) / float(F[3]) > AFMax:
        filterPos.append(F[0] + '\t' + F[1])

hPileupFile.close()


hMismatchFile = open(mismatchFile, 'r')
for line in hMismatchFile:
    F = line.rstrip('\n').split('\t')

    if F[0] + '\t' + F[2] not in filterPos:
        print "\t".join(F)

hMismatchFile.close()

