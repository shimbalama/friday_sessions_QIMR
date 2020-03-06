#!/usr/bin/env python3
import gzip
import pysam
from Bio import SeqIO
from collections import Counter, defaultdict
import scipy.stats as stats
import operator
import pandas as pd
import argparse
import sys

def main ():

    parser = argparse.ArgumentParser(description='somatic var caller')

    required = parser.add_argument_group(
            'Required',
            'ref and pileups')

    required.add_argument(
            '-r',
            '--ref',
            type=str,
            help='ref 37 or 38 [38]',
            default = '/reference/genomes/GRCh38_no_alt_analysis_set/primary_files/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa')

    required.add_argument(
            '-c',
            '--cancer_pile',
            type=str,
            help='pileup of tumour/cancer')

    required.add_argument(
            '-n',
            '--normal_pile',
            type=str,
            help='pileup of normal/blood')

    optional = parser.add_argument_group(
            'Optional',
            'threads and chroms')

    optional.add_argument(
            '-x',
            '--chrom',
            type=str,
            help='Which chromosomes to query. comma,separated,list or [all]',
            default='all')

    args = parser.parse_args()

    print (f'args {args}')
    '''
    Some useful code:

    #Define what chroms you want
    if args.chrom == 'all':
        chroms = ['chr' + str(i+1) for i in range(22)] + ['chrX', 'chrY']
    else:
        chroms = args.chrom.split(',')
    
    #Parse tabix
    for pos in tabixfile.fetch('chr' + str(self.chrom), self.start, self.end):
        tmp_d = dict(zip(keys, pos.split()))
        ...
    
    # variant call with fisher
    oddsratio, pvalue1 = stats.fisher_exact([
        [tumour_count, normal_count],
        [non_base_tumour, non_base_normal]],
        alternative='greater')
  
    #parse ref fasta
    for record in SeqIO.parse(args.ref, 'fasta'):
        if record.id in chroms:
            for i in range(0, len(record.seq), size):
                ...
    '''

if __name__ == '__main__':
    main()
