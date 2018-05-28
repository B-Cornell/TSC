# We find the tree history of each halo at a few redshifts
import numpy as np
import math
import sys

#user enters which snapshot they are interested in
redshift = int(sys.argv[1])
print 'Redshift: ' + str(redshift)


f=open('full_tree_data_'+str(redshift)+'.txt', 'w')

row_id, rockstarId, snapnum, x, y, z, vx, vy, vz, Mvir, Rvir, depthFirstId, mainLeaf_depthFirstId = np.loadtxt('CSVFilesML/BigMDPL_6E13_' + str(redshift) + '_mainleaf.csv', delimiter = ',', unpack = True, skiprows = 1)#this data is sorted by mainleafid

#list to save all tree data for each halo in
treehistorydata = [0,0,0,0,0,0,0,0,[0]*(7*(redshift-10))]

#iterate through all halos at the desired redshift
for og in range(20):#len(row_id)):
    #save the appropriate data in the current redshift to the treehistory list
    treehistorydata[0] = mainLeaf_depthFirstId[og]
    treehistorydata[1] = depthFirstId[og]
    treehistorydata[2] = x[og]
    treehistorydata[3] = y[og]
    treehistorydata[4] = z[og]
    treehistorydata[5] = vx[og]
    treehistorydata[6] = vy[og]
    treehistorydata[7] = vz[og]

    #iterate through all redshifts before the current one
    i = 10
    while i < redshift:
        print i
        trow_id, trockstarId, tsnapnum, tx, ty, tz, tvx, tvy, tvz, tMvir, tRvir, tdepthFirstId, tmainLeaf_depthFirstId = np.loadtxt('CSVFilesML/BigMDPL_6E13_' + str(i) + '_mainleaf.csv', delimiter = ',', unpack = True, skiprows = 1) # this data is sorted by mainleafid
        #now use algorithm to find the appropriate halo that matches the og halo's mainleaf at this previous redshift
        new = 0
        while tmainLeaf_depthFirstId[new] <= mainLeaf_depthFirstId[og]:
            if tmainLeaf_depthFirstId[new] == mainLeaf_depthFirstId[og]:
                treehistorydata[8][(i-10)*3] = tdepthFirstId[new]
                treehistorydata[8][((i-10)*3)+1] = tx[new]
                treehistorydata[8][((i-10)*3)+2] = ty[new]
                treehistorydata[8][((i-10)*3)+3] = tz[new]
                treehistorydata[8][((i-10)*3)+4] = tvx[new]
                treehistorydata[8][((i-10)*3)+5] = tvy[new]
                treehistorydata[8][((i-10)*3)+6] = tvz[new]
            new += 1


        i += 1


#write out the final data. should be one halo per line
f.write(str(treehistorydata) + '\n')
