#! /usr/bin/env python

import sys
import numpy as np
from pyopenms import *

# MS1 feature detection function

def screen(name):

    results = []

    options = PeakFileOptions()
    options.setMSLevels([1])
    fh = MzMLFile()
    fh.setOptions(options)

    # loading the data
    input_map = MSExperiment()
    fh.load(name, input_map)
    input_map.updateRanges()

    # generating params for feature finder
    ff = FeatureFinder()
    ff.setLogType(LogType.CMD)

    prof_type = "centroided"
    features = FeatureMap()
    seeds = FeatureMap()
    params = FeatureFinder().getParameters(prof_type)

    # running feature finder
    ff.run(prof_type, input_map, features, params, seeds)

    # storing the features onto an xml formatted file
    features.setUniqueIds()
    fh = FeatureXMLFile()
    fh.store("{}.featureXML".format(name), features)

    # returning RT, MZ, and Intensities
    rt_mz_int = [ [ f.getRT(), f.getMZ(), f.getIntensity() ] for f in features ]

    np.savetxt('{}.features.tsv'.format(name), rt_mz_int, delimiter=' ', header='RT MZ Intensity')


if __name__ == '__main__':
    screen(sys.argv[1])



