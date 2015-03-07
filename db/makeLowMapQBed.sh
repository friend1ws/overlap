#! /bin/sh
#$ -S /bin/sh
#$ -cwd

# create list of uncertain mapping quality region bed file
# basically, the list is created from the UCSC annotation data
# but also add custom myMappability.bed, 
# which is empirically low mapping quality region after alignment and checking the mapping quality by BWA MEM 

wget http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/microsat.txt.gz
wget http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/simpleRepeat.txt.gz
wget http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/genomicSuperDups.txt.gz
wget http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/hg38ContigDiff.txt.gz
wget http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/hg19ContigDiff.txt.gz

gunzip microsat.txt.gz
gunzip simpleRepeat.txt.gz
gunzip genomicSuperDups.txt.gz
gunzip hg38ContigDiff.txt.gz
gunzip hg19ContigDiff.txt.gz


echo "python broaden.py microsat.txt 5 | mergeBed -i - >  microsat.bed"
python broaden.py microsat.txt 5 | mergeBed -i - >  microsat.bed

echo "python broaden.py simpleRepeat.txt 5 | mergeBed -i - > simpleRepeat.bed"
python broaden.py simpleRepeat.txt 5 | mergeBed -i - > simpleRepeat.bed

echo "python broaden.py genomicSuperDups.txt 5 | mergeBed -i - > genomicSuperDups.bed"
python broaden.py genomicSuperDups.txt 5 | mergeBed -i - > genomicSuperDups.bed

echo "python broaden.py hg38ContigDiff.txt 5 | mergeBed -i - > hg38ContigDiff.bed"
python broaden.py hg38ContigDiff.txt 5 | mergeBed -i - > hg38ContigDiff.bed

echo "python broaden.py hg19ContigDiff.txt 5 | mergeBed -i - > hg19ContigDiff.bed"
python broaden.py hg19ContigDiff.txt 5 | mergeBed -i - > hg19ContigDiff.bed

echo "cat genomicSuperDups.bed simpleRepeat.bed microsat.bed hg38ContigDiff.bed hg19ContigDiff.bed myMappability.bed | sort -k 1,1 -k2,2n - | bedtools merge -i - > lowMapQ.bed"
cat genomicSuperDups.bed simpleRepeat.bed microsat.bed hg38ContigDiff.bed hg19ContigDiff.bed myMappability.bed | sort -k 1,1 -k2,2n - | bedtools merge -i - > lowMapQ.bed 
 
