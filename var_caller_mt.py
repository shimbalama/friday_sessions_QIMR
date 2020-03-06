#!/usr/bin/env python3
from multiprocessing import Pool, TimeoutError
from glob import glob
import gzip
import pysam
from Bio import SeqIO
from collections import Counter, defaultdict
import scipy.stats as stats
import operator
import pandas as pd
import argparse
import cProfile
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
            help='ref 37 or 38 [38]')

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

    optional.add_argument(
            '-t',
            '--threads',
            type=int,
            help='Threads [5]',
            default=8)
    

    args = parser.parse_args()


    if args.chrom == 'all':
        chroms = ['chr' + str(i+1) for i in range(22)] + ['chrX', 'chrY']
    else:
        chroms = args.chrom.split(',')
        
    chunks = chunk_ref(args, chroms)
    print (f'len chunks {len(chunks)}')
    d={}
    with Pool(processes=args.threads) as pool:
        tmp = [(args, chunk) for chunk in chunks]
        res = pool.map(doit, tmp)
        for vars in res:
            d = {**d, **vars}

    df = pd.DataFrame.from_dict(d, orient='index')
    df.to_csv('test.tsv', sep='\t')

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
  
    '''

def doit(tup):

    #https://stackoverflow.com/questions/53890693/cprofile-causes-pickling-error-when-running-multiprocessing-python-code
    args, genomic_region = tup
    print (genomic_region)



def chunk_ref(args, chroms):

    '''
    Split ref into chunks for threading
    '''
    #make server mode where just takes one chrom and scatters with WDL

    chunks = []
    size = 100000 #just for testing, put back to 1mb
    total_len = 0
    for record in SeqIO.parse(args.ref, 'fasta'):
        if record.id in chroms:
            for i in range(0, len(record.seq), size):
                if len(record.seq) > i + size:
                    end = i + size
                else:#end of chrom
                    end = len(record.seq)
                chunks.append((record.id, i, i+size))
                
    return chunks

if __name__ == '__main__':
    main()
