import numpy as np
import sys

snapnum = sys.argv[1]


row, rockstar, snap, x, y, z, vx, vy, vz, mass, rad, dfId, mlId = np.loadtxt('CSVFiles_X/BigMDPL_6E13_' + str(snapnum) + '_x.csv', unpack = True, delimiter = ',', skiprows = 1)

dummyarray = [ [0] for dummy in range(len(row))]





for k in range(len(row)):
    dummyarray[k][0] = row[k]
    dummyarray[k].append(mlId[k])
    dummyarray[k].append(dfId[k])
    dummyarray[k].append(mass[k])


for snapshot in range(10,int(snapnum)+1):
    print snapshot
    MLA, DFA, MassA, MLB, DFB, MassB, Sep, Par, Perp = np.loadtxt('CloseHalos/close_halo_' + str(snapshot) + '.txt', unpack = True, delimiter = ',', skiprows = 1)


    for OGHalo in range(len(row)):


        begin = x[OGHalo] - 200
        if begin < 0:
            begin = 0
        begin = float(begin)/2500. * float(len(MLA))
        begin = int(begin)


        end = x[OGHalo] + 200
        end = float(end)/2500. * float(len(MLA))
        end = int(end)
        if end >= len(MLA):
            end = len(MLA) - 1

        #print percentage done with this snapshot
        if OGHalo%2000 == 0:
            print float(OGHalo)/float(len(row))







        for TreePair in range(begin,end):
            if MLA[TreePair] == mlId[OGHalo]:
                dummyarray[OGHalo].append(snapshot)
                dummyarray[OGHalo].append(DFA[TreePair])
                dummyarray[OGHalo].append(MLB[TreePair])
                dummyarray[OGHalo].append(DFB[TreePair])
                dummyarray[OGHalo].append(MassA[TreePair])
                dummyarray[OGHalo].append(MassB[TreePair])
                dummyarray[OGHalo].append(Sep[TreePair])
                dummyarray[OGHalo].append(Par[TreePair])
                dummyarray[OGHalo].append(Perp[TreePair])
            if MLB[TreePair] == mlId[OGHalo]:
                dummyarray[OGHalo].append(snapshot)
                dummyarray[OGHalo].append(DFB[TreePair])
                dummyarray[OGHalo].append(MLA[TreePair])
                dummyarray[OGHalo].append(DFA[TreePair])
                dummyarray[OGHalo].append(MassB[TreePair])
                dummyarray[OGHalo].append(MassA[TreePair])
                dummyarray[OGHalo].append(Sep[TreePair])
                dummyarray[OGHalo].append(Par[TreePair])
                dummyarray[OGHalo].append(Perp[TreePair])
f = open('singletreehistory' + str(sys.argv[1]) + '.txt', 'w')
for OGHalo in range(len(row)):
    f.write(str(dummyarray[OGHalo][0]))
    for k in range(1,len(dummyarray[OGHalo])):
        f.write(', ' + str(dummyarray[OGHalo][k]))

    f.write('\n')






#'''
