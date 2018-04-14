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


'''Transformations, rotations.
: author Karl Diedrich, PhD <ktdiedrich@gmail.com>
'''

import numpy as np


def xRotation(t):
    '''
    : return rotation matrix 
'''    
    return np.array([ [1.0, 0.0,       0.0],
                      [0.0, np.cos(t), -np.sin(t)],
                      [0.0, np.sin(t), np.cos(t) ] ])

def yRotation(t):
    '''
    : return y rotation matrix 
'''
    return np.array([ [np.cos(t),  0.0, np.sin(t)],
                      [0.0,        1.0, 0.0],
                      [-np.sin(t), 0.0, np.cos(t) ] ])

def zRotation(t):
    '''
    : return z rotation matrix 
'''
    return np.array([ [np.cos(t), -np.sin(t), 0.0],
                      [np.sin(t), np.cos(t),  0.0],
                      [0.0,       0.0,        1.0 ] ])

def rotation(rx, ry, rz):
    '''Combined rotation matrix
    : rx rotation around x axis 
    : ry rotation around y axis 
    : rz rotation around z axis
    : return 3 axis rotation matrix 
'''
    xRot = xRotation(rx)
    yRot = yRotation(ry)
    zRot = zRotation(rz) 
    rot = np.matmul(yRot, xRot)
    rot = np.matmul(zRot, rot)
    return rot

class Rotation:
    '''
'''
    def __init__(self, matrix):
        '''
'''
        self._matrix = matrix
        
    def rotate(self, point):
        '''
'''
        trans = np.dot(self._matrix, point)
        return trans 

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, value):
        self._matrix = value 

if __name__ == '__main__':
    xDeg = 30.0
    yDeg = 45.0
    zDeg = 60.0
    xRad = np.radians(xDeg)
    yRad = np.radians(yDeg)
    zRad = np.radians(zDeg)


    xRot = xRotation(xRad)
    yRot = yRotation(yRad)
    zRot = zRotation(zRad)
    xyzRot = rotation(xRad, yRad, zRad)
    
    print("{} degrees = {} radians, rotation:\n {}".format(xDeg, xRad, xRot))
    print("{} degrees = {} radians, rotation:\n {}".format(yDeg, yRad, yRot))
    print("{} degrees = {} radians, rotation:\n {}".format(zDeg, zRad, zRot))
    print("x, y, z, rotation:\n{}".format(xyzRot))

    rotator = Rotation(matrix=xyzRot)
    xUnit = np.array((1.0, 0.0, 0.0))
    yUnit = np.array((0.0, 1.0, 0.0))
    zUnit = np.array((0.0, 0.0, 1.0))

    xTransformed = rotator.rotate(xUnit)
    yTransformed = rotator.rotate(yUnit)
    zTransformed = rotator.rotate(zUnit)
    print("xUnit {} rotated to {}".format(xUnit, xTransformed))
    print("yUnit {} rotated to {}".format(yUnit, yTransformed))
    print("zUnit {} rotated to {}".format(zUnit, zTransformed))
    
    
