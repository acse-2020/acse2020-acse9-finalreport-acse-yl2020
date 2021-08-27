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
#-------------------------------------------------#
#-- Function to read data in a text file         -#
#-------------------------------------------------#
def ReadData(path,filename,extension):

    output = []

    sf = open(path+filename+extension, 'r')
    data = sf.readlines()

    for i in range(0,len(data)):
        x = str.split(data[i])
        y = [float(v) for v in x]
        output.append(y)
    return output

#-------------------------------------------------#
#-- Function to initialise vtk files             -#
#-------------------------------------------------#
def Initialisation(filename):

    # Read file
    print ('     Read file')
    if filename[-4:] == ".vtu":
        gridreader=vtk.vtkXMLUnstructuredGridReader()
    elif filename[-5:] == ".pvtu":
        gridreader=vtk.vtkXMLPUnstructuredGridReader()
    gridreader.SetFileName(filename)
    gridreader.Update()
    ugrid=gridreader.GetOutput()

    return ugrid

#-------------------------------------------------#
#-- Function to initialise probe filter          -#
#-------------------------------------------------#
def InitialisePointData(ugrid, coordinates):

    # Initialise probe
    points = vtk.vtkPoints()
    points.SetDataTypeToDouble()

    # Create points to be extracted
    print ('     Gathering  coordinates')
    NrbPoints = 0
    for nodeID in range(len(coordinates)):
        NrbPoints += 1
        points.InsertNextPoint(coordinates[nodeID][0], coordinates[nodeID][1], coordinates[nodeID][2])

    print ('           Set points into data...')
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    probe = vtk.vtkProbeFilter()

    print ('           Map data into probe...', 'VTK version ::', vtk.vtkVersion.GetVTKMajorVersion(),'.', vtk.vtkVersion.GetVTKMinorVersion())
    if vtk.vtkVersion.GetVTKMajorVersion() <= 5:
        probe.SetInput(polydata)
        probe.SetSource(ugrid)
    else:
        probe.SetInputData(polydata)
        probe.SetSourceData(ugrid)

    probe.Update()
    
    return probe, points, NrbPoints

#-------------------------------------------------#
#-- Function to initialise cell filter           -#
#-------------------------------------------------#
def InitialiseCellLocator(ugrid):

    # Initialise locator
    print ('     Initialise cell Locator')
    CellLocator = vtk.vtkCellLocator()
    CellLocator.SetDataSet(ugrid)
    CellLocator.Update()
    
    return CellLocator

#--------------------------------------------------#
#-- Function to find the nodes linked to one node -#
#--------------------------------------------------#
def nodesLinkedToNode(nodeID, ugrid):
    nodeIDs = []
    idlist = vtk.vtkIdList()
    ugrid.GetPointCells(nodeID,idlist)
    cellsID_to_nodeID = np.array([idlist.GetId(k) for k in range(idlist.GetNumberOfIds())]) # give all the cells asociated with this node

    for cellID in cellsID_to_nodeID:
        idlist = vtk.vtkIdList()
        ugrid.GetCellPoints(cellID,idlist)
        nodesID_to_cellID = np.array([idlist.GetId(k) for k in range(idlist.GetNumberOfIds())]) # give all the nodes asociated with this cell

        for nodeID_tmp in nodesID_to_cellID:
            if nodeID_tmp not in nodeIDs and nodeID_tmp != nodeID: nodeIDs = np.append(nodeIDs, nodeID_tmp)

    nodeIDs = np.int64(nodeIDs)

    return nodeIDs
#-------------------------------------------------#
#-- Function to do the rotation                  -#
#-------------------------------------------------#
def Rotation(coord_old, theta, x_centre, y_centre):
    
    rotation = np.array([[np.cos(np.radians(theta)), -np.sin(np.radians(theta))],
                        [ np.sin(np.radians(theta)), np.cos(np.radians(theta))]])
    tmp = np.array(coord_old)[:,[0,1]] - [x_centre, y_centre]
    tmp = np.dot(tmp,rotation)
    tmp = tmp + [x_centre, y_centre]
    coord_new = np.append(tmp,np.array(coord_old)[:,[2]], axis=1)

    return coord_new


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
    vtuID     = 0 #-- The mesh is fixed - no need to loop over vtu files

    #-- influenceArea is the number to be changed to include more nodes, 
    #-- i.e. to extend the influence area
    #-- 0 means that the nodes defining the cell in which the sensor is are outputted, i.e. 3/4 nodes in 2D/3D
    #-- 1 means that the nodes defining the adjacent cells are taken into account
    #-- 2 means that the nodes defining the adjacent cells of the adjacent cells are taken into account...
    #-- See theinfluenceAreaSensors.pptx
    influenceArea = 0

    #--------------------------------#
    #-- Geometry input variables   --#
    #--------------------------------#
    #-------------------------#
    #-- DO NOT MODIFY BELOW --#
    #-------------------------#
    # Geometry variables
    Pi = np.pi

    theta = 110.0  # Angle of rotation

    #-- Size of the building in which the room is
    lz_box1 = 9.0  # Length in the z-direction
    lx_box1 = 48.0 # Length in the x-direction
    ly_box1 = 8.11 # Length in the y-direction

    #-- Position of the building in which the room is
    dx_box = 20.0 * lz_box1 # x Position
    dy_box = 6.0  * lz_box1 # y Position
    dz_box = 0.0            # z Position

    e_room  = 0.5 # Thickness of the walls 50cm

    #-- Centre of the building (needed for rotation)
    x_centre = dx_box + lx_box1
    y_centre = dy_box + ly_box1
    print ('x_centre', x_centre, 'y_centre', y_centre)

    #-- Parameters to define the room
    x_room = 42.2    # x position of the left hand side corner
    y_room = e_room  # y position of the left hand side corner
    z_room = 6.08    # z position of the left hand side corner

    #-- Dimensions of the room
    lx_room = 5.3  # Length of the room
    ly_room = 7.11 # Width of the room
    lz_room = 2.42 # Height of the room

    #-- Min and max coordiantes of the room - before rotation
    xmin = dx_box+x_room
    xmax = dx_box+x_room+lx_room
    ymin = dy_box+y_room 
    ymax = dy_box+y_room+ly_room 
    zmin = dz_box+z_room
    zmax = dz_box+z_room+lz_room

    print ('Before Coordinate Rotation')
    print ('xmin::', xmin, ' xmax::', xmax)
    print ('ymin::', ymin, ' ymax::', ymax)
    print ('zmin::', zmin, ' zmax::', zmax)

    # --------------------------#
    # -- Coordinates Fluidity --#
    #---------------------------#
    coordinates = []

    tap1 = [xmax-1.0,  ymin+0.1,  zmin+0.9]
    tap2 = [xmax-4.3,  ymin+0.1,  zmin+0.9]
    tap3 = [xmax-1.7,  ymin+7.0,  zmin+0.9]
    tap4 = [xmax-0.1 , ymin+4.14, zmin+1.2]
    tap5 = [xmax-5.2 , ymin+3.14, zmin+1.22]
    tap6 = [xmax-4.53, ymin+6.17, zmin+2.4]
    tap7 = [xmax-2.65, ymin+4.14, zmin+0.79]

    coord_init = np.array([tap1,  tap2,  tap3,  tap4,  tap5,  tap6,  tap7])

    print ('\n Coordinates Concentration Init::')
    print (coord_init)

    coordinates = Rotation(coord_init, theta, x_centre, y_centre)

    print ('\n Coordinates Concentration ::')
    print (coordinates)

    #-- Write Coordinates

    # sys.exit('\n EXIT HERE')

    #---------------------------------------------------------------------
    # EXTRACT DATA
    #---------------------------------------------------------------------
    tic = time.time()

    filename=path+name_simu+'_'+str(vtuID)+extension
    print ('\n\n  '+str(filename))
    
    # Read file
    ugrid = Initialisation(filename)

    # Initialise probe
    probe, points, NrbPoints = InitialisePointData(ugrid, coordinates)

    # Initialise cell location
    CellLocator = InitialiseCellLocator(ugrid)

    #-- Check Validity of points
    print ('           Check point Validity')
    valid_ids = probe.GetOutput().GetPointData().GetArray('vtkValidPointMask')
    validPoints = vtktools.arr([valid_ids.GetTuple1(i) for i in range(NrbPoints)])
    print ('           ... ', len(validPoints)-np.sum(validPoints), 'invalid points')
    
    nodeIDs = []

    # Extract data
    print ('     Extract Data')
    for sensorID in range(len(coordinates)):
        print ('\n   For sensor ', sensorID+1)        
        coordSensor = [coordinates[sensorID][0], coordinates[sensorID][1], coordinates[sensorID][2]]
        cellID =  CellLocator.FindCell(coordSensor) # cell ID which contains the sensor
        idlist=vtk.vtkIdList()
        ugrid.GetCellPoints(cellID, idlist)
        array_tmp = np.array([idlist.GetId(j) for j in range(idlist.GetNumberOfIds())])

        array_all = array_tmp
        print (array_all)

        area_tmp = 0

        while area_tmp != influenceArea:
            print ('     For influence area level ::', area_tmp+1)
            for nodeID in array_tmp:
                nodeIDs_tmp = nodesLinkedToNode(nodeID, ugrid)
                array_all=np.append(array_all,nodeIDs_tmp)
                array_all=np.unique(array_all)

            array_tmp = array_all
            print (array_all)

            area_tmp += 1
    
        np.savetxt('Sensor'+str(sensorID+1)+'_NodeIDs.dat',array_all, fmt='%i')
            
    toc = time.time()

    print ('\n\nTime : ', toc - tic, 'sec')
