# We find the tree history of each halo at a few redshifts
import numpy as np
import pandas as pd
import math
import sys

#user enters which snapshot they are interested in
redshift = int(sys.argv[1])
print 'Redshift: ' + str(redshift)

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

data = pd.read_csv('CSVFilesML/BigMDPL_6E13_' + str(redshift) + '_mainleaf.csv')#this data is sorted by mainleafid
data['history'] = pd.Series([0]*(redshift-11) for row in data.iterrows())

#iterate through all redshifts before the current one
for snapshot in range(11,redshift):
    print snapshot
    pastdata = pd.read_csv('CSVFilesML/BigMDPL_6E13_' + str(snapshot) + '_mainleaf.csv') # this data is sorted by mainleafid

    #now use algorithm to find the appropriate halo that matches the og halo's mainleaf at this previous redshift
    for row in data.itertuples():
        mainleafcheck = binarysearch(pastdata.mainLeaf_depthFirstId, row.mainLeaf_depthFirstId)
        if mainleafcheck != 0:
            row.history[(snapshot-11)] = pastdata.iloc[mainleafcheck]
data.to_csv('full_tree_data_'+str(redshift)+'.csv', index = False)
#'''
