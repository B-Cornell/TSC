import numpy as np
import sys
import pandas as pd
import math
import matplotlib.pyplot as plt


for snapshot in range(12,80):
    df = pd.read_csv('singletreehistory/singletreehistory%2d.txt' %snapshot)
    nomerge = 0
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


    weights = [0.424, 0.219, 0.461, 0.278, 0.038, 0.098, 0.037, 0.097, 0.048, 0.084, 0.047, 0.094, 0.047, 0.093, 0.045, 0.091, 0.046, 0.100, 0.044, 0.099, 0.044, 0.097, 0.043, 0.095, 0.052, 0.094, 0.078, 0.192, 0.049, 0.137, 0.096, 0.199, 0.092, 0.199, 0.097, 0.191, 0.101, 0.092, 0.099, 0.105, 0.095, 0.094, 0.100, 0.099, 0.104, 0.096, 0.100, 0.099, 0.098, 0.102, 0.094, 0.099, 0.103, 0.095, 0.100, 0.104, 0.095, 0.100, 0.097, 0.102, 0.099, 0.102, 0.095, 0.103, 0.096, 0.098, 0.233, 0.489, 1.450]

    hist, bins = np.histogram(passinghist, bins = int(snapshot)-9)
    print hist

    for i in range(len(hist)-1):
        hist[i+1] = float(hist[i+1])/float(weights[-(i+1)])

    plt.plot(hist)
    plt.yscale('log')
    plt.ylabel('Major Merger Events / Time')
    plt.xlabel('TimeSteps')
    plt.show()


    plt.plot(hist)
    plt.ylabel('Major Merger Events / Time')
    plt.xlabel('TimeSteps')
    plt.show()
#'''
