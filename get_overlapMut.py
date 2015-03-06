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

    # get overlapping coordinates
    overlatStart = 0
    overlatEnd = 0
    if int(F1[3]) < int(F2[3]):
        overlapStart = int(F2[3])
        seqlen1 = re.match('(\d+)M', F1[5]).group(1)
        overlapEnd = int(F1[3]) + int(seqlen1) - 1
    else:
        overlapStart = int(F1[3])
        seqlen2 = re.match('(\d+)M', F2[5]).group(1)
        overlapEnd = int(F2[3]) + int(seqlen2) - 1

    # get mismatch positions
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
            if tempPos >= overlapStart and tempPos <= overlapEnd:
                pos2mis1[tempPos] = item.group(2)
            tempPos += 1

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
            if tempPos >= overlapStart and tempPos <= overlapEnd:
                pos2mis2[tempPos] = item.group(2)
            tempPos += 1

    misPosList = list(set(pos2mis1.keys() + pos2mis2.keys()))
    if len(misPosList) == 0:
        continue

    for misPos in misPosList:

        # get the basic information for both read
        ID = F1[0]
        chr = F1[2]
        pos1 = int(F1[3])
        pos2 = int(F2[3])
        mapQ1 = int(F1[4])
        mapQ2 = int(F2[4])
        seqlen1 = int(re.match('(\d+)M', F1[5]).group(1))
        seqlen2 = int(re.match('(\d+)M', F2[5]).group(1))

        ##########
        # get the strand and read number information from the flag
        flags1 = format(int(F1[1]), '#014b')[:2:-1] 
        if flags1[0] == 0 or flags1[1] == 0 or flags1[4] == flags1[5] or flags1[6] == flags1[7]:
            print F1
            print "inconsistency of the flag!"
            sys.exit()
        readNum1 = 1 if flags1[6] == "1" else 2
        dir1 = "+" if flags1[4] == "0" else "-"

        flags2 = format(int(F2[1]), '#014b')[:2:-1]
        if flags2[0] == 0 or flags2[1] == 0 or flags2[4] == flags2[5] or flags2[6] == flags2[7]:
            print F2
            print "inconsistency of the flag!" 
            sys.exit()
        readNum2 = 1 if flags2[6] == "1" else 2
        dir2 = "+" if flags2[4] == "0" else "-"

        # check for the inconsistency
        if dir1 == dir2:
            print flags1, flags2
            print dir1, dir2
            print "inconsistency of the alignment direction!"
            sys.exit()

        if readNum1 == readNum2:
            print flags1, flags2
            print readNum1, readNum2
            print "inconsistency of the readNumber"
            sys.exit()

        key1 = chr + "," + str(pos1) + "," + dir1 + "," + str(mapQ1)
        key2 = chr + "," + str(pos2) + "," + dir2 + "," + str(mapQ2)
        ##########

        # get the information on nucleotides, base quality and cycle number
        ind1 = misPos - pos1
        ind2 = misPos - pos2
        cycle1 = ind1 if dir1 == "+" else seqlen1 - ind1 - 1
        cycle2 = ind2 if dir2 == "+" else seqlen2 - ind2 - 1
        nuc1 = (F1[9])[max(0, (ind1 - 10)):ind1] + "~" + (F1[9])[ind1:(ind1 + 1)] + "~" + (F1[9])[(ind1 + 1):(ind1 + 11)]
        nuc2 = (F2[9])[max(0, (ind2 - 10)):ind2] + "~" + (F2[9])[ind2:(ind2 + 1)] + "~" + (F2[9])[(ind2 + 1):(ind2 + 11)]
        baseQ1 = (F1[10])[max(0, (ind1 - 10)):ind1] + "~" + (F1[10])[ind1:(ind1 + 1)] + "~" + (F1[10])[(ind1 + 1):(ind1 + 11)]
        baseQ2 = (F2[10])[max(0, (ind2 - 10)):ind2] + "~" + (F2[10])[ind2:(ind2 + 1)] + "~" + (F2[10])[(ind2 + 1):(ind2 + 11)]

        # get the reference and alternative base information
        ref = ""
        if misPos in pos2mis1:
            ref = pos2mis1[misPos]
        elif misPos in pos2mis2:
            ref = pos2mis2[misPos]
        else:
            print "something is wrong!"
            print F1
            print F2
            print sys.exit()
        alt1 = (F1[9])[ind1:(ind1 + 1)]
        alt2 = (F2[9])[ind2:(ind2 + 1)]

        # print the result
        if readNum1 == 1 and readNum2 == 2:
            print "\t".join([chr, str(misPos), ref, alt1, alt2, str(cycle1), str(cycle2), nuc1, nuc2, baseQ1, baseQ2, key1, key2, ID])
        elif readNum1 == 2 and readNum2 == 1:
            print "\t".join([chr, str(misPos), ref, alt2, alt1, str(cycle2), str(cycle1), nuc2, nuc1, baseQ2, baseQ1, key2, key1, ID])
        else:
            print flags1, flags2 
            print readNum1, readNum2
            print "inconsistency of the readNumber"
            sys.exit()
   

inFile.close()


