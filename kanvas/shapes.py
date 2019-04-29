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
from kanvas.canvas import Renderer, RenderWindow, Box 

class ArrowFactory:
    '''Make arrows 
'''
    def __init__(self, shaftRadius=0.05, tipLength=0.2):
        '''Set arrow parameters 
'''
        self._shaftRadius = shaftRadius
        self._tipLength = tipLength

    def makeArrow(self):
        '''Make arrow with current parameter settings 
'''
        arrow = vtk.vtkArrowSource()
        arrow.SetShaftRadius(self._shaftRadius)
        
        arrow.SetTipLength(self._tipLength)
        return arrow

    @property
    def shaftRadius(self):
        return self._shaftRadius

    @shaftRadius.setter
    def shaftRadius(self, value):
        self._shaftRadius = value
        
    @property
    def tipLength(self):
        return self._tipLength

    @tipLength.setter
    def tipLength(self, value):
        self._tipLength = value

    
class ConeFactory:
    '''Cone 
'''
    def __init__(self, height=3.0, radius=1.0, resolution=20):
        '''Initialize settings for making cones 
'''
        self._height = height
        self._radius = radius
        self._resolution = resolution

    def makeCone(self):
        '''Make a cone with the current settings 
'''
        cone = vtk.vtkConeSource()
        cone.SetHeight(self._height)
        cone.SetRadius(self._radius)
        cone.SetResolution( self._resolution)
        return cone 
    
    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value

    @property
    def resolution(self):
        return self._resolution

    @resolution.setter
    def resolution(self, value):
        self.resolution = value

def parabola3D(x, y, k=-1.5, c=0.0):
    '''
'''
    return (k* (x**2 + y**2) ) + c 

if __name__ == '__main__':

    coneFactory = ConeFactory()
    arrowFactory = ArrowFactory()

    renderWindow = RenderWindow(size=(800, 400), BoxClass=Box)
    #rwBox = renderWindow.box
    #print(rwBox)
    
    renderer1 = Renderer()
    # renderer1.renderer.ResetCamera()
    camera1 = renderer1.renderer.GetActiveCamera()
    # vtkCamera settings:
    # https://www.vtk.org/doc/nightly/html/classvtkCamera.html#ac1dcd796574d6b2abcade341587838c2
    camera1.Elevation(-30)
    camera1.Dolly(.2)
    
    # renderer1.renderer.Dolly(30)
    renderer1.addCallback(renderWindow.azimuthCallback)

    actorProperty1 = vtk.vtkProperty()
    actorProperty1.SetColor(.6, .2, .2)
    actorProperty1.SetDiffuse(.7)
    actorProperty1.SetSpecular(.4)
    actorProperty1.SetSpecularPower(20)

    renderer1.addActorSource(arrowFactory.makeArrow(), actorProperty=actorProperty1,
                             position=(0.25, -.1, 0) )

    property3 = vtk.vtkProperty()
    property3.SetColor(.4, 0, .4)
    renderer1.addActorSource(vtk.vtkCubeSource(), actorProperty=property3,
                             position=(0.1, 1, -1.5))

    renderer2 = Renderer(background=(.1, .2, .2))
    property2 = vtk.vtkProperty()
    property2.SetColor(.2, .2, .8)
    renderer2.addActorSource(coneFactory.makeCone(), actorProperty=property2, position=(0, 0, 0), box=None)
    renderer2.renderer.ResetCamera()
    camera2 = renderer2.renderer.GetActiveCamera()
    camera2.Azimuth(75)
    # camera2.Dolly(.75)
    camera2.Elevation(40)
    

    renderWindow.addRenderer(renderer1, (0.0, 0.0, 0.5, 1.0))
    renderWindow.addRenderer(renderer2, (0.5, 0.0, 1.0, 1.0))
    # renderWindow.addRenderer(renderer2, (0.0, 0.0, 1.0, 1.0))
    
    # rwBox.boxWidget.On()
    renderWindow.rotate()
    renderWindow.renderInteractive()
    
