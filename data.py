import pandas as pd
import numpy as np
import math

for snapshot in range(10,39):#10-80 once fully functional
    twopasses = 0
    onepasses = 0
    zeropasses = 0
    bigpasses = 0

    data= pd.read_pickle('FullTreeHistory/full_tree_history_%2d.pkl' %snapshot)
    for row in data.itertuples():#each row has one halo and all of it's attributes
        passes = 0
        if row.history != []: #empty lists means no merger history
            snaplist = row.history[0::11]
            mlidalist = row.history[2::11]
            massalist = row.history[4::11]
            mlidblist = row.history[5::11]
            massblist = row.history[7::11]
            seplist = row.history[8::11]
            onvellist = row.history[9::11]
            offvellist = row.history[10::11]
            if len(snaplist) != len(mlidalist):
                print 'fuckin a'
            if len(snaplist) != len(mlidblist):
                print ' '
                print row.history
                print mlidblist

            for mainleaf in set(mlidalist + mlidblist):
                newseplist = []
                newonvellist = []
                newoffvellist = []
                if mainleaf != row.mainLeaf_depthFirstId:
                    for i in range(len(snaplist)):
                        if (mlidalist[i] == mainleaf or mlidblist[i] == mainleaf):
                            newseplist.append(seplist[i])
                            newonvellist.append(onvellist[i])
                            newoffvellist.append(offvellist[i])
                    #check if it merged in it's past
                    for time in range(1,len(newseplist)-1):
                        #counts as a pass through if it is at a local minimum and has less than a 500kpc separation
                        if newseplist[time] < newseplist[time+1] and newseplist[time] < newseplist[time-1] and newseplist[time] < .5:
                            #compute the angle the velocity vector makes with the separation vector
                            pass_rel_vel_angle = math.atan(abs(newoffvellist[time]/newonvellist[time]))
                            #calculate the estimated pericenter distance based on the data from the closest snapshot we have
                            pericenter = newseplist[time]*math.sin(pass_rel_vel_angle)
                            passes += 1
                    #check if it merged in the last time step
                    if len(newseplist) > 3:
                        #say that it had a merger event if it is currently outbound, is less that 500kpc separation
                        if newseplist[-1] < newseplist[-2] and newseplist[-1] < .5 and newonvellist[-1] > 0:
                            #compute the angle the velocity vector makes with the separation vector
                            pass_rel_vel_angle = math.atan(abs(newoffvellist[-1]/newonvellist[-1]))
                            #calculate the estimated pericenter distance based on the data from the closest snapshot we have
                            pericenter = newseplist[-1]*math.sin(pass_rel_vel_angle)
                            passes += 1
        if passes == 0:
            zeropasses += 1
        elif passes == 1:
            onepasses += 1
        elif passes == 2:
            twopasses += 1
        else:
            bigpasses += 1
    print snapshot
    print 'Zero Passes: %2d' %zeropasses
    print 'One Pass:    %2d' %onepasses
    print 'Two Passes:  %2d' %twopasses
    print 'Big Passes:  %2d' %bigpasses
    print ''



#'''
