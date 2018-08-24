import numpy as np
import pandas as pd
import sys


for snapshot in range(10,80):
    print '%2d              ' %snapshot
    data = pd.read_csv('CSVFiles_X/BigMDPL_6E13_%2d_x.csv' %snapshot)
    data['history'] = pd.Series([] for row in data.iterrows())
    for ss in range(10,snapshot+1):
        sys.stdout.write('%2d\r' %ss)
        sys.stdout.flush()
        ssdata = pd.read_csv('CloseHalos/close_halo_%2d.txt' %ss)
        for row in data.itertuples():
            for altrow in ssdata.itertuples():
                if row.mainLeaf_depthFirstId == altrow.mlida or row.mainLeaf_depthFirstId == altrow.dfida:
                    row.history.append(ss)
                    row.history.append(altrow)
    data.to_csv('full_tree_history_%2d.csv' %snapshot, index = False)






#'''
