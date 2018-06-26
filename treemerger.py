import numpy as np
import sys
import pandas as pd
import math
import matplotlib.pyplot as plt




snapshot = sys.argv[1]




df = pd.read_csv('singletreehistory/singletreehistory' + str(snapshot) + '.txt', sep="|", names=['A'])
cols = list('ABCDE')
df[cols] = df.A.str.split(',', n=4, expand=True)
df.E = df.E.str.split(',')

nomerge = 0
numtreeshist = []
passinghist = []
for x in range(len(df.E)):
    if x % 1000 == 0:
        print float(x)/float(len(df.E))
    if df.E[x] == None:
        nomerge +=1
        #numtreeshist.append(0)
    else:
        #print '\n\ntree'
        num_trees = len(df.E[x]) / 9
        numtreeshist.append(num_trees)
        mainleafs = []
        #Snap, DFA, MLB, DFB, MassA, MassB, Sep, Par, Perp
        for a in range(num_trees):
            if [df.E[x][2+(a*9)]] not in mainleafs:
                mainleafs.append([df.E[x][2+(a*9)]])
        #print mainleafs
        for a in range(len(mainleafs)):
            for b in range(num_trees):
                if df.E[x][2+(b*9)] == mainleafs[a][0]:
                    mainleafs[a].append(float(df.E[x][(b*9)]))
                    #mainleafs[a].append(float(df.E[x][1+(b*9)]))
                    #mainleafs[a].append(float(df.E[x][3+(b*9)]))
                    mainleafs[a].append(float(df.E[x][4+(b*9)]))
                    mainleafs[a].append(float(df.E[x][5+(b*9)]))
                    mainleafs[a].append(float(df.E[x][6+(b*9)]))
                    mainleafs[a].append(float(df.E[x][7+(b*9)]))
                    mainleafs[a].append(float(df.E[x][8+(b*9)]))
        #put all the mainleaf lists through the merger tests
        for list in mainleafs:
            #print "pair"
            passes = 0
            seplist = []
            onvellist = []
            offvellist = []
            snaplist = []
            numberofhalos = (len(list)-1)//6
            for spoopy in range(numberofhalos):
                seplist.append(list[4+spoopy*6])
                onvellist.append(list[5+spoopy*6])
                offvellist.append(list[6+spoopy*6])
                snaplist.append(list[1+spoopy*6])


            #print seplist
            for time in range(1,len(seplist)-1):
                if seplist[time] < seplist[time+1] and seplist[time] < seplist[time-1] and seplist[time] < .5:
                    pass_rel_vel_angle = math.atan(abs(offvellist[time]/onvellist[time]))
                    pericenter = seplist[time]*math.sin(pass_rel_vel_angle)
                    passes += 1
                    passinghist.append(snaplist[time])

                if len(seplist) > 3:
                    #say that it had a merger event if it is currently outbound, is less that 500kpc separation
                    if seplist[-1] < seplist[-2] and seplist[-1] < .5 and onvellist[-1] > 0:
                        #compute the angle the velocity vector makes with the separation vector
                        pass_rel_vel_angle = math.atan(abs(offvellist[-1]/onvellist[-1]))
                        #calculate the estimated pericenter distance based on the data from the closest snapshot we have
                        pericenter = seplist[-1]*math.sin(pass_rel_vel_angle)
                        passes += 1
                        passinghist.append(snaplist[-1])
            #print passes


plt.hist(passinghist, bins = 68)
plt.show()
#'''
