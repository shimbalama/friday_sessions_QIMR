#!/usr/bin/env python3
#from multiprocessing import Pool, TimeoutError
from glob import glob
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

    args = parser.parse_args()

def func1():
    pass
    

if __name__ == '__main__':
    main()
