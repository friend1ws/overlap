#! /usr/local/bin/python

import sys
inputFile = sys.argv[1]
EitherOrBoth = int(sys.argv[2]) # 1: the overlap mismatches, 2: the overlap matches
cycleMin = int(sys.argv[3])
cycleMax = int(sys.argv[4])
baseMin = int(sys.argv[5])

hInputFile = open(inputFile, 'r')
for line in hInputFile:
    F = line.rstrip('\n').split('\t')

    if EitherOrBoth == 1 and F[4] == F[5]:
        continue

    if EitherOrBoth == 2 and F[4] != F[5]:
        continue


    if int(F[6]) < cycleMin or int(F[6]) > cycleMax or int(F[7]) < cycleMin or int(F[7]) > cycleMax:
        continue

    base_ascii1 = F[10].split('~')
    base_ascii2 = F[11].split('~')

    base_ord1_prev = map(lambda x: ord(x) - 33, base_ascii1[0])
    base_ord1_center = map(lambda x: ord(x) - 33, base_ascii1[1])
    base_ord1_after = map(lambda x: ord(x) - 33, base_ascii1[2])

    base_ord2_prev = map(lambda x: ord(x) - 33, base_ascii2[0])
    base_ord2_center = map(lambda x: ord(x) - 33, base_ascii2[1])
    base_ord2_after = map(lambda x: ord(x) - 33, base_ascii2[2])

    if min(base_ord1_prev + base_ord1_center + base_ord1_after + base_ord2_prev + base_ord2_center + base_ord2_after) < baseMin:
        continue

    print '\t'.join(F)

hInputFile.close()
 
