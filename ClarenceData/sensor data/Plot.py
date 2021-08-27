#!/usr/bin/env python3.8

#//////////////////////////////////////////////////////
#-- Dr Laetitia Mottet
#     Applied Modelling and Computation Group
#     Department of Earth Science and Engineering
#     Imperial College London
#     l.mottet@imperial.ac.uk
#     laetitia.mottet@gmail.com
#//////////////////////////////////////////////////////

# # # ########################## # # #
# # # ######  LIBRARIES   ###### # # #
# # # ########################## # # #
from numpy import *
from math  import *
import sys, os
sys.path.append("/home/lmottet/fluidity-temp/python/")
import numpy as np
import vtk
import vtktools
import matplotlib.pyplot as plt
import datetime, time

# # # ########################## # # #
# # # ######  FUNCTIONS   ###### # # #
# # # ########################## # # #
#-------------------------------------------------#
#-- Function to read data in a text file         -#
#-------------------------------------------------#
def ReadData(filename):
    output = []
    sf = open(filename, 'r')
    data = sf.readlines()
    for i in range(0,len(data)):
        x = str.split(data[i])
        y = [float(v) for v in x]
        output.append(y)

    output = np.transpose(output)
    return output


# # # ########################## # # #
# # # ######    MAIN      ###### # # #
# # # ########################## # # #
if __name__ == '__main__':
    tic = time.time()

    CO2_Fluidity = ReadData('CO2_Fluidity.dat')
    print ('CO2_Fluidity ::', CO2_Fluidity)

    CO2_Experiment = ReadData('CO2_Experiment.dat')
    print ('CO2_Experiment ::', CO2_Experiment)

    #-----------------------#
    #-- PLTOS             --#
    #-----------------------#
    figID = 0
    #--------------#
    #-- FIGURE 1 --#
    #--------------#
    #-- Plot Fluidity data only
    figID += 1
    plt.figure(figID)
    ax = plt.subplot(111)

    colorSt = ['black', 'magenta', 'green', 'red', 'yellow', 'cyan', 'orange']
    lineSt  = ['-', '-', '-', '-', '-', '-', '-'] 

    #-------------------------#
    #-- Plot Fluidity data  --#
    #-------------------------#
    for sensorID in range(0,7):
        plt.plot(CO2_Fluidity[0], CO2_Fluidity[sensorID+1], color=colorSt[sensorID],   linestyle=lineSt[sensorID],  marker=' ', label='Sensor '+str(sensorID+1)+' (CFD)')

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.22), ncol=3, fontsize=10,fancybox=True, shadow=True)
    plt.title('Fluidity CO2',y=1.23)
    plt.xlabel('Time (sec.)')
    plt.ylabel('CO2 (ppm)')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width , box.height* 0.85])
    axes = plt.gca()
    axes.set_ylim(400,1600)
    axes.set_xlim(0,1500)
    plt.grid()
    plt.savefig('CO2_Fluidity.svg')
    plt.close()

    #--------------#
    #-- FIGURE 2 --#
    #--------------#
    #-- Plot Experiment data only
    figID += 1
    plt.figure(figID)
    ax = plt.subplot(111)

    colorSt = ['black', 'magenta', 'green', 'red', 'yellow', 'cyan', 'orange']
    lineSt  = ['-', '-', '-', '-', '-', '-', '-'] 

    #-------------------------#
    #-- Plot Experiment data  --#
    #-------------------------#
    for sensorID in range(0,7):
        plt.plot(CO2_Experiment[0], CO2_Experiment[sensorID+1], color=colorSt[sensorID],   linestyle=lineSt[sensorID],  marker=' ', label='Sensor '+str(sensorID+1)+' (Exp)')

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.22), ncol=3, fontsize=10,fancybox=True, shadow=True)
    plt.title('Experiment CO2',y=1.23)
    plt.xlabel('Time (sec.)')
    plt.ylabel('CO2 (ppm)')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width , box.height* 0.85])
    axes = plt.gca()
    axes.set_ylim(400,1600)
    axes.set_xlim(0,1500)
    plt.grid()
    plt.savefig('CO2_Experiment.svg')
    plt.close()

    #--------------#
    #-- FIGURE 3 --#
    #--------------#
    #-- Plot Experiment and Fluidity for one sensor on 1 plot
    colorSt = ['black', 'magenta', 'green', 'red', 'yellow', 'cyan', 'orange']
    lineSt  = ['-', '-', '-', '-', '-', '-', '-'] 
    for sensorID in range(0,7):
        figID += 1
        plt.figure(figID)
        ax = plt.subplot(111)

        #-------------------------#
        #-- Plot Fluidity data  --#
        #-------------------------#
        plt.plot(CO2_Fluidity[0], CO2_Fluidity[sensorID+1], color=colorSt[sensorID], linestyle='-',  marker=' ', label='Sensor '+str(sensorID+1)+' (CFD)')

        #-------------------------#
        #-- Plot Experiment data  --#
        #-------------------------#
        plt.plot(CO2_Experiment[0], CO2_Experiment[sensorID+1], color=colorSt[sensorID], linestyle='--',  marker=' ', label='Sensor '+str(sensorID+1)+' (Exp)')

        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.22), ncol=3, fontsize=10,fancybox=True, shadow=True)
        plt.xlabel('Time (sec.)')
        plt.ylabel('CO2 (ppm)')
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width , box.height* 0.85])
        axes = plt.gca()
        axes.set_ylim(400,1600)
        axes.set_xlim(0,1500)
        plt.grid()
        plt.savefig('CO2_FluidityExperiment_sensor'+str(sensorID+1)+'.svg')
        plt.close()                     

    #--------------#
    #-- FIGURE 4 --#
    #--------------#
    #-- Plot Experiment and Fluidity data
    figID += 1
    plt.figure(figID)
    ax = plt.subplot(111)

    colorSt = ['black', 'magenta', 'green', 'red', 'yellow', 'cyan', 'orange']
    lineSt  = ['-', '-', '-', '-', '-', '-', '-'] 

    #-------------------------#
    #-- Plot Fluidity data  --#
    #-------------------------#
    for sensorID in range(0,7):
        plt.plot(CO2_Fluidity[0], CO2_Fluidity[sensorID+1], color=colorSt[sensorID],   linestyle='-',  marker=' ', label='Sensor '+str(sensorID+1)+' (CFD)')

    #-------------------------#
    #-- Plot Experiment data  --#
    #-------------------------#
    for sensorID in range(0,7):
        plt.plot(CO2_Experiment[0], CO2_Experiment[sensorID+1], color=colorSt[sensorID],   linestyle='--',  marker=' ', label='Sensor '+str(sensorID+1)+' (Exp)')

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.22), ncol=3, fontsize=10,fancybox=True, shadow=True)
    plt.xlabel('Time (sec.)')
    plt.ylabel('CO2 (ppm)')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width , box.height* 0.85])
    axes = plt.gca()
    axes.set_ylim(400,1600)
    axes.set_xlim(0,1500)
    plt.grid()
    plt.savefig('CO2_FluidityExperiment.svg')
    plt.close()

    toc = time.time()

    print ('\n\nTime : ', toc - tic, 'sec')
