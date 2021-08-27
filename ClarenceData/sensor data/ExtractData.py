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
import numpy as np
import vtk
import vtktools
import matplotlib.pyplot as plt
import datetime, time

# # # ########################## # # #
# # # ######  FUNCTIONS   ###### # # #
# # # ########################## # # #



# # # ########################## # # #
# # # ######    MAIN      ###### # # #
# # # ########################## # # #
if __name__ == '__main__':
    tic = time.time()

    #--------------------------------#
    #-- Choose variables           --#
    #--------------------------------#
    # Vtu files
    path      = '../Simu/run_Clip_ToSend/'
    extension = '.vtu'
    name_simu = 'ClarenceCentre'
    fieldname = 'CO2_ppm'
    vtu_start = 0
    vtu_end   = 5
    vtu_step  = 1

    #---------------------------------------------------------------------
    # EXTRACT DATA
    #---------------------------------------------------------------------
    for vtuID in range(vtu_start,vtu_end,vtu_step):
        filename=path+name_simu+'_'+str(vtuID)+extension
        print ('\n\n  '+str(filename))

        vtu_data = vtktools.vtu(filename)
        data     = vtu_data.GetField(fieldname)
        print (data)

    print ('\n\nTime : ', toc - tic, 'sec')