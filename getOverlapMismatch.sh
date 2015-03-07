#! /bin/sh
#$ -S /bin/sh
#$ -cwd
#$ -e log/ -o log/

INPUTBAM=$1
REGION=$2
OUTPUT=$3

export PATH=${PATH}:/home/yshira/bin/tabix-0.2.6
export PATH=${PATH}:/home/yshira/bin/samtools-0.1.18
export PATH=${PATH}:/home/yshira/bin/bedtools2-2.22.0/bin

export PYTHONHOME=/usr/local/package/python2.7/2.7.8
export PATH=${PYTHONHOME}/bin:${PATH}
export LD_LIBRARY_PATH=${PYTHONHOME}/lib:${LD_LIBRARY_PATH}

REFERENCE=/home/yshira/common/ref/hg19_all/hg19.all.fasta

if [ ! -d log ]
    mkdir log
fi

# remove the short reads whose alignment is uncertain in terms of genomic annotations
# and select the short reads by the specified region
echo "bedtools intersect -abam ${INPUTBAM} -b db/lowMapQ.bed -v | samtools view -h - ${REGION} > ${OUTPUT}.tmp.bam"
bedtools intersect -abam ${INPUTBAM} -b db/lowMapQ.bed -v | samtools view -h - ${REGION} > ${OUTPUT}.tmp.bam 

echo "samtools index ${OUTPUT}.tmp.bam"
samtools index ${OUTPUT}.tmp.bam

echo "samtools view ${OUTPUT}.tmp.bam > ${OUTPUT}.tmp.sam"
samtools view ${OUTPUT}.tmp.bam > ${OUTPUT}.tmp.sam


# get the overlapping short reads
echo "python get_overlapRead.py ${OUTPUT}.tmp.sam 40 150 > ${OUTPUT}.tmp.readpair"
python get_overlapRead.py ${OUTPUT}.tmp.sam 40 150 > ${OUTPUT}.tmp.readpair 

# get the mismatch position within the overlapping reads
echo "python get_overlapMut.py ${OUTPUT}.tmp.readpair > ${OUTPUT}.tmp.mis"
python get_overlapMut.py ${OUTPUT}.tmp.readpair > ${OUTPUT}.tmp.mis


# select the db142 data for the specified region
echo "tabix db/snp142.single.bed.gz ${REGION} > ${OUTPUT}.tmp.snp.bed"
tabix db/snp142.single.bed.gz ${REGION} > ${OUTPUT}.tmp.snp.bed

# remove the mismatch position registered in dbsnp142
echo "bedtools intersect -a test.mis -b snp.bed -v > ${OUTPUT}.tmp.mis.filt1"
bedtools intersect -a test.mis -b snp.bed -v > ${OUTPUT}.tmp.mis.filt1


# check the pileup information for the mismatch position 
echo "samtools mpileup -B -d10000000 -f ${REFERENCE} -q 0 -Q 40 -l ${OUTPUT}.tmp.mis.filt1 ${OUTPUT}.tmp.bam > ${OUTPUT}.tmp.pileup"
samtools mpileup -B -d10000000 -f ${REFERENCE} -q 0 -Q 40 -l ${OUTPUT}.tmp.mis.filt1 ${OUTPUT}.tmp.bam > ${OUTPUT}.tmp.pileup

# filter by depth and allele frequency
echo "python alleleFreqDepthFilt.py ${OUTPUT}.tmp.mis.filt1 ${OUTPUT}.tmp.pileup 10 500 0.1 > ${OUTPUT}.tmp.mis.filt2"
python alleleFreqDepthFilt.py ${OUTPUT}.tmp.mis.filt1 ${OUTPUT}.tmp.pileup 10 500 0.1 > ${OUTPUT}.tmp.mis.filt2


