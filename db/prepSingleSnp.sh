#! /bin/sh

wget http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/snp142.txt.gz
gunzip snp142.txt.gz 

echo "python getSingleSnp.py snp142.txt > snp142.single.bed"
python getSingleSnp.py snp142.txt > snp142.single.bed

echo "bgzip snp142.single.bed"
bgzip snp142.single.bed 

echo "tabix -p bed -f snp142.single.bed.gz"
tabix -p bed -f snp142.single.bed.gz

