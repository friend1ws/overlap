#! /usr/local/bin/python

import sys, re
inputFile = sys.argv[1]

inFile = open(inputFile, "r")

MDRe = re.compile('(\d*)([ACGT])')
while True:

    line1 = inFile.readline()
    if not line1:
        break
    row1 = line1.rstrip('\n')
    F1 = row1.split('\t')

    line2 = inFile.readline()
    if not line2:
        break
    row2 = line2.rstrip('\n')
    F2 = row2.split('\t')

    if F1[0] != F2[0]:
        print "%s %s, inconsistency of a read pair!" % (F1[0], F2[0])
        sys.exit()
   

    remainRow1 = "\t".join(F1[11:])
    remainRow2 = "\t".join(F2[11:])
    pos2mis1 = {} 
    pos2mis2 = {} 

    if re.search('NM:i:0', remainRow1) is None:
        tempMD = re.search('MD:Z:([\d\w]+)', remainRow1)
        if tempMD is None:
            print "Sam File has some inconsistency..! No MD:Z: tag"
            print row1
            sys.exit()
        misInfo = MDRe.finditer(tempMD.group(1))
        tempPos = int(F1[3])
        for item in misInfo:
            tempPos += int(item.group(1))
            pos2mis1[tempPos] = item.group(2)

    if re.search('NM:i:0', remainRow2) is None:
        tempMD = re.search('MD:Z:([\d\w]+)', remainRow2)
        if tempMD is None:
            print "Sam File has some inconsistency..! No MD:Z: tag"
            print row2
            sys.exit()
        misInfo = MDRe.finditer(tempMD.group(1))
        tempPos = int(F2[3])
        for item in misInfo:
            tempPos += int(item.group(1))
            pos2mis2[tempPos] = item.group(2)

                
    if len(pos2mis1) > 0 or len(pos2mis2) > 0:
        print row1
        print row2

inFile.close()

"""
HWI-ST1289:327:H8VFCADXX:2:1114:2143:21750  163 chr1    13352245    47  161M    =   13352269    185 CCTGCTCCCCAGAGGCCATGAGTAAAAGGCAGACAGTGGAGGACTGTCCAAGGATGGGAGAGTGCCAGCCCTTGAAGGTGTTCATAGACCGCTGCCTAAAGAAAAGTACACTGGATGAATGCCTGAGCTACCTCTGTGGGTAGATCCACTACAGAAGAGGT   CCCFFFFFGHHHHIBEHGIJCHAFHHICFHIIIGHGGHG>DF@DCA8DGEFHEEEHHC=55;.=EH;?BDAEECEDDD5;A?ADCDCDCCBB@BBBDDDCD@AC?C4:ACDDCBCCCDCCCDC>CA?CAACCCCCCAADD9C04@CC>?>9?>ACDA>BB#   NM:i:0  MD:Z:161    AS:i:161    XS:i:156
"""

