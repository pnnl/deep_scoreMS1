#! /usr/bin/env python

import sys
import pandas as pd
import numpy as np
import glob

def screen():

    pids = []
    psms = []

    for i in glob.glob('perc_output/*'):
        df = pd.read_csv(i, sep='\t')
        peptides = df[df['percolator q-value'] <= 0.01 ]['sequence']
        hits = [i for i in peptides]

        if len(hits) >= 1:
            psms.append(hits)
            pids.append(i.replace('perc_output/', '').replace('.percolator.target.psms.txt', ''))

    with open('pids_successful.txt', 'w') as f:
        for item in pids:
            f.write('%s\n' % item)
                            
if __name__ == '__main__':
    screen()
