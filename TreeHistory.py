# We find the tree history of each halo at a few redshifts
import numpy as np
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

def sep(i,j):
    separation = math.sqrt( ((x[i]-x[j])*(x[i]-x[j])) + ((y[i]-y[j])*(y[i]-y[j])) + ((z[i]-z[j])*(z[i]-z[j])))
    return separation


f=open('full_tree_data_'+str(redshift)+'.txt', 'w')

row_id, rockstarId, snapnum, x, y, z, vx, vy, vz, Mvir, Rvir, depthFirstId, mainLeaf_depthFirstId = np.loadtxt('CSVFilesML/BigMDPL_6E13_' + str(redshift) + '_mainleaf.csv', delimiter = ',', unpack = True, skiprows = 1)#this data is sorted by mainleafid

#list to save all tree data for each halo in
treehistorydata = [[0,0,0,0,0,0,0,0,0,[0]*(7*(redshift-11))] for dummy in range(len(row_id))]

#iterate through all halos at the desired redshift
for og in range(len(row_id)):
    #save the appropriate data in the current redshift to the treehistory list
    treehistorydata[og][0] = mainLeaf_depthFirstId[og]
    treehistorydata[og][1] = depthFirstId[og]
    treehistorydata[og][2] = Mvir[og]
    treehistorydata[og][3] = x[og]
    treehistorydata[og][4] = y[og]
    treehistorydata[og][5] = z[og]
    treehistorydata[og][6] = vx[og]
    treehistorydata[og][7] = vy[og]
    treehistorydata[og][8] = vz[og]



#iterate through all redshifts before the current one
i = 11
while i < redshift:
    print i
    trow_id, trockstarId, tsnapnum, tx, ty, tz, tvx, tvy, tvz, tMvir, tRvir, tdepthFirstId, tmainLeaf_depthFirstId = np.loadtxt('CSVFilesML/BigMDPL_6E13_' + str(i) + '_mainleaf.csv', delimiter = ',', unpack = True, skiprows = 1) # this data is sorted by mainleafid

    #now use algorithm to find the appropriate halo that matches the og halo's mainleaf at this previous redshift
    for og in range(len(row_id)):
        mainleafcheck = binarysearch(tmainLeaf_depthFirstId, mainLeaf_depthFirstId[og])
        if mainleafcheck != 0:
            treehistorydata[og][9][(i-11)*7] = tMvir[mainleafcheck]
            treehistorydata[og][9][((i-11)*7)+1] = tx[mainleafcheck]
            treehistorydata[og][9][((i-11)*7)+2] = ty[mainleafcheck]
            treehistorydata[og][9][((i-11)*7)+3] = tz[mainleafcheck]
            treehistorydata[og][9][((i-11)*7)+4] = tvx[mainleafcheck]
            treehistorydata[og][9][((i-11)*7)+5] = tvy[mainleafcheck]
            treehistorydata[og][9][((i-11)*7)+6] = tvz[mainleafcheck]

    i += 1

for og in range(len(row_id)):
    if treehistorydata[og][9] != [0]*(7*(redshift-11)):
        f.write(str(treehistorydata[og][0]) + ', ' + str(treehistorydata[og][1]) + ', ' + str(treehistorydata[og][2]) + ', ' + str(treehistorydata[og][3]) + ', ' + str(treehistorydata[og][4]) + ', ' + str(treehistorydata[og][5]) + ', ' + str(treehistorydata[og][6]) + ', ' + str(treehistorydata[og][7]) + ', ' + str(treehistorydata[og][8]))
        for entry in range(len(treehistorydata[og][9])):
            f.write(', ' + str(treehistorydata[og][9][entry]))
        f.write('\n')
