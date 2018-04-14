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


'''Drawing functions
: author Karl T. Diedrich, PhD <ktdiedrich@gmail.com>
'''

import vtk 
import time 

class Box:
    '''Box widget around interactor 
'''
    def __init__(self, interactor, placeFactor=1.25):
        self._boxWidget = vtk.vtkBoxWidget()
        self._boxWidget.SetInteractor(interactor)
        self._boxWidget.SetPlaceFactor(placeFactor)

    def setActor(self, actor):
        '''Observer actor's InteractionEvent's 
'''
        # print("setActor {}".format(actor))
        self._boxWidget.SetProp3D(actor)
        self._boxWidget.PlaceWidget()
        self._boxWidget.AddObserver("InteractionEvent", self.boxCallback)
        self._boxWidget.On()
        

    def boxCallback(self, widget, eventString):
        '''Transform box in response to event 
'''
        t = vtk.vtkTransform()
        self._boxWidget.GetTransform(t)
        self._boxWidget.GetProp3D().SetUserTransform(t)

    @property
    def boxWidget(self):
        return self._boxWidget

    
class RenderWindow:
    '''
'''
    def __init__(self, size=(300, 300), sleepTime=0.03, azimuthStep=1, renderer=None,
                 interactorStyle=vtk.vtkInteractorStyleTrackballCamera(), BoxClass=None ):
        self._size = size
        self._sleepTime = sleepTime
        self._azimuthStep = azimuthStep
        self._rotation = 0
        self._box = None
        
        self._renderWindow = vtk.vtkRenderWindow()
        self._renderWindow.SetSize(self._size)
        self._renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        self._renderWindowInteractor.SetRenderWindow(self._renderWindow)
        if interactorStyle:
            self.interactorStyle = interactorStyle
        if BoxClass:
            self._box = Box(interactor=self._renderWindowInteractor)
        
        self._renderers = []
        if renderer:
            self.addRenderer(renderer)

    @property
    def box(self):
        return self._box
    
    @property
    def interactorStyle(self):
        return self._interactorStyle

    @interactorStyle.setter
    def interactorStyle(self, value):
        self._interactorStyle = value
        self._renderWindowInteractor.SetInteractorStyle(value)
        
    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self._renderWindow.SetSize(self._size)

    def addRenderer(self, renderer, viewport=(0,0,1,1)):
        renderer.renderer.SetViewport(viewport[0], viewport[1], viewport[2], viewport[3])
        self._renderers.append(renderer.renderer)
        self._renderWindow.AddRenderer(renderer.renderer)
    
    def renderInteractive(self):
        '''Render displaying source objects. 
    '''
        self._renderWindow.Render()
        self._renderWindowInteractor.Initialize() 
        self._renderWindowInteractor.Start()

    def rotate(self):
        '''Rotate scene in a circle 
'''
        for self._rotation in range(0, 360):
            time.sleep(self._sleepTime)
            self._renderWindow.Render()
            for ren in self._renderers:
                ren.GetActiveCamera().Azimuth(self._azimuthStep)

    def azimuthCallback(self, obj, string):
        '''Print the current azimuth 
'''
        # print("Current azimuth {}".format(self._rotation * self._azimuthStep))
        pass 

    @property
    def rotation(self):
        return self._rotation
    
    @property
    def sleepTime(self):
        return self._sleepTime

    @sleepTime.setter
    def sleepTime(self, value):
        self._sleepTime = value 

    @property
    def azimuth(self):
        return self._azimuth

    @azimuth.setter
    def azimuth(self, value):
        self._azimuth = value 


class Actor:
    '''Default parameters for an actor 
'''
    def __init__(self, source, zMin=-10.0, zMax=10.0, actorProperty=None,
                 position=(0,0,0), box=None, scale=1.0 ):
        '''Set up default actor parameters 
'''
        self._mapper = vtk.vtkPolyDataMapper()
        self._source = source
        if type(self._source) == vtk.vtkPolyData:
            self._mapper.SetInputData(self._source )
            self._mapper.SetColorModeToDefault()
            self._mapper.SetScalarRange(zMin, zMax)
            self._mapper.SetScalarVisibility(1)
        else:
            self._mapper.SetInputConnection(self._source.GetOutputPort())
        self._actor = vtk.vtkActor()
        if scale:
            self._actor.SetScale(scale)
        if actorProperty:
            self._actor.SetProperty(actorProperty)
        if position:
            self._actor.SetPosition(position[0], position[1], position[2])
        self._actor.SetMapper(self._mapper)
        if box:
            box.setActor(self._actor)

    @property
    def actor(self):
        return self._actor

    @property
    def mapper(self):
        return self._mapper

    @property
    def source(self):
        return self._source 
    
class Renderer:
    '''
'''
    def __init__(self, source=None, background=(0.1, 0.2, 0.3), zMin=-10.0, zMax=10.0 ):
        '''Render a shape with interacor
    :windowSize (x pixels, y pixels)

'''
        self._renderer = vtk.vtkRenderer()
        self._renderer.SetBackground(background[0], background[1], background[2])
        self._box = None
        self._zMin = zMin
        self._zMax = zMax 
        
        if source:
            self.addActorSource(source)
        
    def addActorSource(self, source, actorProperty=None, position=None, box=None, scale=None):
        '''Add addition source shapes as actors to the renderer. Creates actor.
        : source VTK object source 
'''
        actor = Actor(source=source, zMin=-10.0, zMax=10.0, actorProperty=actorProperty,
                 position=position, box=box, scale=scale)
        self._renderer.AddActor(actor.actor)

    def addActor(self, actor):
        '''Add actor to renderer directly 
'''
        if type(actor) == type(vtk.vtkActor()):
            self._renderer.AddActor(actor)
        elif type(actor) == Actor:
            self._renderer.AddActor(actor.actor)
        else:
            print("addActor unknown type ")
        
    def addCallback(self, callback, event="StartEvent"):
        '''Add a callback function 
'''
        self._renderer.AddObserver("StartEvent", callback)
        
    @property
    def renderer(self):
        return self._renderer

    @property
    def box(self):
        return self._box

    @box.setter
    def box(self, value):
        self._box = value
    
if __name__ == '__main__':
    renderWindow = RenderWindow(size=(400, 400), BoxClass=Box)
    rwBox = renderWindow.box

    cone = vtk.vtkConeSource()
    cone.SetHeight(5.0)
    cone.SetRadius(1.0)
    cone.SetResolution(50)
    
    renderer1 = Renderer(background=(.1, .2, .2))
    property1 = vtk.vtkProperty()
    property1.SetColor(.3, .2, .2)

        
    renderer1.addActorSource(cone, actorProperty=property1, position=(0, 0, 0), box=rwBox)
    renderer1.renderer.ResetCamera()
    camera1 = renderer1.renderer.GetActiveCamera()
    camera1.Azimuth(10)
    # camera1.Dolly(1.2)
    camera1.Elevation(-10)
    
    renderWindow.addRenderer(renderer1, (0.0, 0.0, 1.0, 1.0))
    
    rwBox.boxWidget.On()
    renderWindow.rotate()
    renderWindow.renderInteractive()
    
