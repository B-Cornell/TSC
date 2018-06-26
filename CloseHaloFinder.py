#Finds all halos within 2Mpc of eachother in each of the snapshots


import numpy as np
import math
import sys


def sep(x1,y1,z1,x2,y2,z2):
    separation = math.sqrt( ((x1-x2)*(x1-x2)) + ((y1-y2)*(y1-y2)) + ((z1-z2)*(z1-z2)) )
    return separation

for snapnum in range(10,79):
    f = open('close_halo_' + str(snapnum) + '.txt', 'w')
    print snapnum
    row, rockstar, snap, x, y, z, vx, vy, vz, mass, rad, dfId, mlId = np.loadtxt('CSVFiles_X/BigMDPL_6E13_' + str(snapnum) + '_x.csv', unpack = True, delimiter = ',', skiprows = 1)
    endoflist = False
    for k in range(len(row)):
        if k % 1000 == 0:
            print float(k)/float(len(row))
        j = k + 1

        if endoflist == False:
            while (x[j] < (x[k] + 2)):
                separation = sep(x[j],y[j],z[j],x[k],y[k],z[k])
                if separation < 2:
                    relative_velocity = math.sqrt( ((vx[k]-vx[j])**2) + ((vy[k]-vy[j])**2) + ((vz[k]-vz[j])**2) );
                    Vel_par = ((vx[k]-vx[j])*(x[k]-x[j])+(vy[k]-vy[j])*(y[k]-y[j])+(vz[k]-vz[j])*(z[k]-z[j]))/separation;
                    Vel_perp = math.sqrt((relative_velocity**2)-(Vel_par**2));

                    f.write( str(mlId[k]) + ', ' + str(dfId[k]) + ', ' + str(mass[k]) + ', ' + str(mlId[j]) + ', ' + str(dfId[j]) + ', ' + str(mass[j]) + ', ' + str(separation) + ', ' + str(Vel_par) + ', ' + str(Vel_perp) + '\n' )
                if x[j] >= 2499:
                    endoflist = True

                j += 1
