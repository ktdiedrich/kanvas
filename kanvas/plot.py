#!/usr/bin/env python3

#=========================================================================
#
#  Copyright (c) 2018  Karl T. Diedrich, PhD
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0.txt
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#=========================================================================*/


import vtk
import numpy as np
from kanvas.canvas import Renderer, RenderWindow, Box, Actor 
from kanvas.shapes import parabola3D, ArrowFactory
from kanvas.transform import Rotation, rotation, xRotation, yRotation, zRotation

'''Plot points in 3D 

: author Karl Diedrich, PhD <ktdiedrich@gmail.com>
'''
class Extent:
    '''Range information 
'''
    def __init__(self, minX0=0, maxX0=0, minY0=0, maxY0=0, minZ0=0, maxZ0=0):
        'Set initial values of range'
        self._minX = minX0
        self._maxX = maxX0
        self._minY = minY0
        self._maxY = maxY0
        self._minZ = minZ0
        self._maxZ = maxZ0
    def __str__(self):
        return "minX={:.3}, maxX={:.3}, minY={:.3}, maxY={:.3}, minZ={:.3}, maxZ={:.3}".format(self._minX, self._maxX,
                self._minY, self._maxY, self._minZ, self._maxZ)
    @property
    def minX(self):
        return self._minX
    @minX.setter
    def minX(self, value):
        if value < self._minX:
            self._minX = value
    @property
    def maxX(self):
        return self._maxX
    @maxX.setter
    def maxX(self, value):
        if value > self._maxX:
            self._maxX = value

    @property
    def minY(self):
        return self._minY
    @minY.setter
    def minY(self, value):
        if value < self._minY:
            self._minY = value
    @property
    def maxY(self):
        return self._maxY
    @maxY.setter
    def maxY(self, value):
        if value > self._maxY:
            self._maxY = value

    @property
    def minZ(self):
        return self._minZ
    @minZ.setter
    def minZ(self, value):
        if value < self._minZ:
            self._minY = value
    @property
    def maxZ(self):
        return self._maxZ
    @maxZ.setter
    def maxZ(self, value):
        if value > self._maxZ:
            self._maxZ = value
   
class PointData:
    def __init__(self, maxNumPoints=1e6):
        '''Points of data kept in class object separate of mapper and actor. 
'''
        self._maxNumPoints = maxNumPoints
        self._vtkPolyData = vtk.vtkPolyData()
        self.clearPoints()
        self._extent = None
        
    def addPoint(self, point):
        if self._vtkPoints.GetNumberOfPoints() < self._maxNumPoints:
            pointId = self._vtkPoints.InsertNextPoint(point[:])
            self._vtkDepth.InsertNextValue(point[2])
            self._vtkCells.InsertNextCell(1)
            self._vtkCells.InsertCellPoint(pointId)
        else:
            r = np.random.randint(0, self.maxNumPoints)
            self._vtkPoints.SetPoint(r, point[:])
        self._vtkCells.Modified()
        self._vtkPoints.Modified()
        self._vtkDepth.Modified()
 
    def clearPoints(self):
        self._vtkPoints = vtk.vtkPoints()
        self._vtkCells = vtk.vtkCellArray()
        self._vtkDepth = vtk.vtkDoubleArray()
        self._vtkDepth.SetName('DepthArray')
        self._vtkPolyData.SetPoints(self._vtkPoints)
        self._vtkPolyData.SetVerts(self._vtkCells)
        self._vtkPolyData.GetPointData().SetScalars(self._vtkDepth)
        self._vtkPolyData.GetPointData().SetActiveScalars('DepthArray')

    @property
    def vtkPolyData(self):
        return self._vtkPolyData

    @property
    def extent(self):
        return self._extent

    @extent.setter
    def extent(self, value):
        self._extent = value 

class VtkPointCloud:
    def __init__(self, zMin=-10.0, zMax=10.0, maxNumPoints=1e6):
        self._pointData = PointData(maxNumPoints=maxNumPoints)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(self._pointData.vtkPolyData )
        mapper.SetColorModeToDefault()
        mapper.SetScalarRange(zMin, zMax)
        mapper.SetScalarVisibility(1)
        self._vtkActor = vtk.vtkActor()
        self._vtkActor.SetMapper(mapper)
 
    def addPoint(self, point):
        self._pointData.addPoint(point)
 
    def clearPoints(self):
        self._pointData.clearPoints() 

    @property
    def vtkActor(self):
        return self._vtkActor 
 
def load_data(filename):
    pointCloud = VtkPointCloud()
    data = np.genfromtxt(filename,dtype=float,skip_header=0,usecols=[0,1,2], delimiter=',')
    for k in range(np.size(data,0)):
        point = data[k] #20*(random.rand(3)-0.5)
        pointCloud.addPoint(point)
    return pointCloud


def makePointCloudActor(xBegin, xEnd, yBegin, yEnd, functZ, step=1.0, dtype=np.float64):
    '''Generate range of points with the functZ function 
'''
    pointCloud = VtkPointCloud()
    for x in np.arange(xBegin, xEnd, step):
        for y in np.arange(yBegin, yEnd, step):
            z = functZ(x, y)
            point =  np.array((x, y, z), dtype=dtype)
            pointCloud.addPoint(point)
    return pointCloud

def makePointData(xBegin, xEnd, yBegin, yEnd, functZ, step=1.0, dtype=np.float64, rotationMatrix=None):
    pointData = PointData()
    rotator = None
    zBegin = functZ(xBegin, yBegin)
    extent = Extent(minX0=xBegin, maxX0=xBegin, minY0=yBegin, maxY0=yBegin, minZ0=zBegin, maxZ0=zBegin)
    if type(rotationMatrix) == np.ndarray:
        rotator = Rotation(rotationMatrix)
    for x in np.arange(xBegin, xEnd, step):
        for y in np.arange(yBegin, yEnd, step):
            z = functZ(x, y)
            point =  np.array((x, y, z), dtype=dtype)
            extent.minX = x
            extent.maxX = x
            extent.minY = y
            extent.maxY = y
            extent.minZ = z
            extent.maxZ = z
            if rotator:
                point = rotator.rotate(point)
            pointData.addPoint(point)
    pointData.extent = extent 
    return pointData 

def makeSpherePoints(r, step=.1, dtype=np.float64):
    '''
'''
    from math import pi, sin, cos  
    pointData = PointData()
    for s in np.arange(0, 2*pi, step):
        for t in np.arange(0, pi, step):
            x = r*cos(s)*sin(t)
            y = r*sin(s)*sin(t)
            z = r*cos(t)
            point = np.array((x,y,z), dtype=dtype)
            pointData.addPoint(point)
    return pointData 
    
def displayPointCloud(pointCloud):
    '''Example
    pointCloud = makePointCloudActor(xBegin=-radius, xEnd=radius, yBegin=-radius, yEnd=radius, functZ=parabola3D, step=step, dtype=np.float64)
    displayPointCloud(pointCloud=pointCloud)
'''
    renderer = vtk.vtkRenderer()
    renderer.AddActor(pointCloud.vtkActor)
#renderer.SetBackground(.2, .3, .4)
    renderer.SetBackground(0.0, 0.0, 0.0)
    renderer.ResetCamera()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindow.Render()
    renderWindow.SetWindowName("XYZ Data Viewer")
    renderWindowInteractor.Start()
    
    
if __name__ == '__main__':
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='Plot 3D points')
    parser.add_argument('--input', type=str, default="/home/ktdiedrich/Documents/dev/Crispersight/python/ktd/test1.csv",
                    help='input CSV file of x,y,z points in rows ')

    args = parser.parse_args()
    print("input {}".format(args.input))
    
    # pointCloud=load_data(args.input)
    radius = 4.0
    step = 0.1
    xDegree = -20.0
    yDegree = -15.0
    zDegree = -20.0
    
    rotationMatrix = rotation(np.radians(xDegree), np.radians(yDegree), np.radians(zDegree))
        
    window = RenderWindow(size=(1200,600))

    parabolaData = makePointData(xBegin=-radius, xEnd=radius, yBegin=-radius, yEnd=radius,
                        functZ=parabola3D, step=step, dtype=np.float64, rotationMatrix=rotationMatrix)
    print("Parabola: {}".format(parabolaData.extent))
    parabolaRenderer = Renderer(background=(.1, .15, .1))
    parabolaRenderer.addActorSource(parabolaData.vtkPolyData, position=(0,0,0))
    
    arrowFactory = ArrowFactory()
    xArrow = arrowFactory.makeArrow()
    yArrow = arrowFactory.makeArrow()
    zArrow = arrowFactory.makeArrow()
    xArrowProp = vtk.vtkProperty()
    xArrowProp.SetColor(.4, .1, .1)

    ext = parabolaData.extent
    scaleFactor = 10
    zPos = (ext.maxZ+ext.minZ)/2.0
    xArrowActor = Actor(source=xArrow, zMin=-10.0, zMax=10.0, actorProperty=xArrowProp,
                 position=(0-scaleFactor, 0, 0), box=None, scale=(scaleFactor, scaleFactor, scaleFactor) )

    parabolaRenderer.addActor(xArrowActor)
    
    
    window.addRenderer(parabolaRenderer, (0.0, 0.0, 0.5, 1.0) )
    

    circleData = makeSpherePoints(r=radius, step=step, dtype=np.float64)
    circleRenderer = Renderer(background=(.15, .1, .1))
    circleRenderer.addActorSource(circleData.vtkPolyData)
    window.addRenderer(circleRenderer, (0.5, 0.0, 1.0, 1.0))
    window.renderInteractive() 
    
