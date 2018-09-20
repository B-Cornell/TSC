import numpy as np
import pandas as pd
import sys
import pickle

def binarysearch(somelist, target):
    first = 0
    last = len(somelist) - 1
    found = False
    while first < last and found == False:
        midp = (first + last)//2
        if somelist[midp] == target:
            found = True
        elif somelist[midp] > target:
            last = midp-1
        else:
            first = midp+1
    if found == True:
        return midp
    else:
        return 0

for snapshot in range(11,80):
    print '%2d              ' %snapshot
    data = pd.read_csv('CSVFilesML/BigMDPL_6E13_%2d_mainleaf.csv' %snapshot)
    data['history'] = pd.Series([] for row in data.iterrows())
    for ss in range(11,snapshot+1):
        sys.stdout.write('%2d\r' %ss)
        sys.stdout.flush()
        ssdata = pd.read_csv('Pairs/snap_%2d.csv' %ss)
        for row in ssdata.itertuples():

            mainleafcheck = binarysearch(data.mainLeaf_depthFirstId, row.mlida)
            if mainleafcheck != 0:
                data.iloc[mainleafcheck].history.append(ss)
                data.iloc[mainleafcheck].history.extend(row)
            mainleafcheck = binarysearch(data.mainLeaf_depthFirstId, row.mlidb)
            if mainleafcheck != 0:
                data.iloc[mainleafcheck].history.append(ss)
                data.iloc[mainleafcheck].history.extend(row)

    data.to_pickle('RawHistory/raw_history_%2d.pkl' %snapshot)

#'''
