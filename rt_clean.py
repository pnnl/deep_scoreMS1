import pandas as pd
import numpy as np

import sys
import time

from pyopenms import *
import argparse
import bisect
from os.path import basename
import re

# function calculates pTIC

def calcTIC(exp):
    tic = 0.0
    for scan in exp:
        if scan.getMSLevel() == 1:
            mz, i = scan.get_peaks()
            tic += sum(i)
    return(tic)

Function normalizes PTIC and selects within the range of 0.05 and 0.95

def norm_trunc(PID):

    feature_map = FeatureMap()
    FeatureXMLFile().load('{}.mzML.featureXML'.format(PID), feature_map)

    options = PeakFileOptions()
    options.setMSLevels([1])

    fh = MzMLFile()
    fh.setOptions(options)
    input_map = MSExperiment()
    fh.load('{}.mzML'.format(PID), input_map)

    totalTic = calcTIC(input_map)

    rtList = []
    pTicList = []
    sumTIC = 0.0
    for scan in input_map:
        if scan.getMSLevel() == 1:
            mz, i = scan.get_peaks()

            rtList.append(scan.getRT())
            pTicList.append(sumTIC/totalTic)
            sumTIC += sum(i)

    feature_list = []

    min_pTIC = .05
    max_pTIC = .95

    for f in feature_map:
        curIntens = f.getIntensity()
        curMz = round(f.getMZ(),4)
        curRt = round(f.getRT(),4)
    
        curIndex = bisect.bisect_left(rtList,curRt)
        leftSideRT = rtList[curIndex-1]
        rightSideRT = rtList[curIndex]

        leftSideDiff = curRt - leftSideRT
        rightSideDiff = rightSideRT - curRt

        pTIC = 0 
    
        if leftSideDiff > rightSideDiff:
            pTIC = round(pTicList[curIndex],4)
        else:
            pTIC = round(pTicList[curIndex-1],4)

        if pTIC >= min_pTIC and pTIC <= max_pTIC:
            feature = (curMz,curRt, curIntens, pTIC)
            feature_list.append(feature)

    ms1_feats = pd.DataFrame(feature_list, columns=['MZ', 'RT', 'Intensity', 'pTIC'])
    ms1_feats.sort_values(by='RT').to_csv('{}_ms1.csv'.format(PID))

if __name__ == '__main__':
    t1 = time.time()
    norm_trunc(PID=sys.argv[1])
    t2 = time.time()
    print("Time Elapsed: ", round(t2-t1, 2), "seconds")
    