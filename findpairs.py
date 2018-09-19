#Modified from the original version by David Wittman
#This finds all the pairs within 5Mpc of eachother in our data

import matplotlib.pyplot as plt
import numpy as np
import math
import sys

# user-settable prefs
maxdist = 5 # Mpc
maxdistsq = maxdist**2


def writeoutput(indx1,indx2):
    # to speed later operations,
    # record halos in numerical order of mainLeaf_depthFirstId
    if ml[indx1]<ml[indx2]:
        i=indx1
        j=indx2
    elif ml[indx1]>ml[indx2]:
        i=indx2
        j=indx1
    else:
        print 'This cannot happen, aborting'
        sys.exit(1)
    f.write('%5.3f %5.3f %5.3f %5.2f %5.2f %5.2f %d %6.4e %d %d %d %5.2e %d %d' % (x[i]-x[j],y[i]-y[j],z[i]-z[j],vx[i]-vx[j],vy[i]-vy[j],vz[i]-vz[j],rockstar[i],mass[i],df[i],ml[i],rockstar[j],mass[j],df[j],ml[j]))
    return

for snapshot in range(11,80):
    #load data
    row, rockstar, snap, x, y, z, vx, vy, vz, mass, rad, df, ml = np.loadtxt('CSVFiles_X/BigMDPL_6E13_' + str(snapshot) + '_x.csv', unpack = True, delimiter = ',', skiprows = 1)

    nhalos = len(row)
    paired = {}
    menageatrois = {}
    sys.stderr.write('Read in %d halos\n' % nhalos)

    j=1
    for k in range(nhalos-1):
        if k%1000 == 0: # progress meter
            sys.stderr.write('%d / %d\r' % (k,nhalos))

        # Look for partner halos at greater x, up to maxdist (remember,
        # input file is sorted by x). Start by just finding the max index
        # for which a calculation will be necessary
        while j<nhalos and x[j]-x[k] < maxdist:
            j += 1
            if j==nhalos:
                break # don't go past end of input catalog!
        # j is now just PAST the last possible match, so we'll the slice :j is relevant
        if j==k+1:
            # the relevant slice has zero length
            continue


        # now use numpy to operate on the slice in one fell swoop
        ispair = (x[k+1:j]-x[k])**2 + (y[k+1:j]-y[k])**2 + (z[k+1:j]-z[k])**2<maxdistsq
        for i in np.where(ispair)[0]:
            mymatch = k+1+i
            if rockstar[k]!=rockstar[mymatch]: # this avoids matching a halo to itself!
                # check/track whether either halo is already in a pair.
                if mymatch in paired:
                    menageatrois[mymatch]=True
                    menageatrois[k]=True
                    menageatrois[paired[mymatch]]=True
                if k in paired:
                    menageatrois[mymatch]=True
                    menageatrois[k]=True
                    menageatrois[paired[k]]=True
                paired[mymatch]=k
                paired[k]=mymatch


    # now output those pairs that are not in menage a trois
    f = open('Pairs/snap_%2d.csv' %snapshot, 'w')
    written = {}
    for halo in paired:
        partner = paired[halo]
        if (partner not in menageatrois) and (halo not in menageatrois) and (halo not in written):
            writeoutput(halo,partner)
            written[partner] = True

    sys.stderr.write('halos in menages: %d\n' % len(menageatrois))
    sys.stderr.write('pairs found: %d\n' % len(written))
