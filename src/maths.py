import math
from math import *
import numpy

def translate(matrix, vector):

    transform = numpy.identity(4, numpy.float32)
    transform[0][3] = vector[0]
    transform[1][3] = vector[1]
    transform[2][3] = vector[2]

    return transform.dot(matrix)

def rotate(matrix, angle, axis):

    transform = numpy.identity(4, numpy.float32)
    axis = normalize(axis)

    u = axis[0]
    v = axis[1]
    w = axis[2]
    u2 = u * u
    v2 = v * v
    w2 = w * w

    transform[0][0] = u2 + ((v2 + w2)*cos(angle))
    transform[0][1] = u*v*(1 - cos(angle)) - w*sin(angle)
    transform[0][2] = u*w*(1 - cos(angle)) + v*sin(angle)
    transform[1][0] = u*v*(1 - cos(angle)) + w*sin(angle)
    transform[1][1] = v2 + (u2 + w2)*cos(angle)
    transform[1][2] = v*w*(1 - cos(angle)) - u*sin(angle)
    transform[2][0] = u*w*(1 - cos(angle)) - v*sin(angle)
    transform[2][1] = v*w*(1 - cos(angle)) + u*sin(angle)
    transform[2][2] = w2 + (u2 + v2)*cos(angle)

    return transform.dot(matrix)

def normalize(vec):

    mod = (sqrt(vec[0]*vec[0] + vec[1]*vec[1] + vec[2]*vec[2]))

    nVec = (vec[0]/mod, vec[1]/mod, vec[2]/mod)
    return nVec

def Scale(matrix, scale):

    transform = numpy.identity(4, numpy.float32)

    transform[0][0] = scale
    transform[1][1] = scale
    transform[2][2] = scale

    return transform.dot(matrix)

def transformationMatrix(vector, angle, scale):

    matrix = numpy.identity(4, numpy.float32)

    matrix = translate(matrix, vector)
    matrix = rotate(matrix, math.radians(angle[0]), (1, 0, 0))
    matrix = rotate(matrix, math.radians(angle[1]), (0, 1, 0))
    matrix = rotate(matrix, math.radians(angle[2]), (0, 0, 1))
    matrix = Scale(matrix, scale)

    return matrix

def projectionMatrix(aspectRatio, FOV, zNear, zFar):

    matrix = numpy.identity(4, numpy.float32)

    yScale = (1/tan(math.radians(FOV/2)))*aspectRatio
    xScale = yScale/aspectRatio
    zP = zFar + zNear
    zM = zFar - zNear
    matrix[0][0] = xScale
    matrix[1][1] = yScale
    matrix[2][2] = -zP/zM
    matrix[2][3] = -1
    matrix[3][2] = -(2*zFar*zNear)/zM
    matrix[3][3] = 0

    return matrix

def viewMatrix(camera1):

    matrix = numpy.identity(4, numpy.float32)
    cameraPos = camera1.getPosition()
    
    matrix = rotate(matrix, math.radians(camera1.getPitch()), (1, 0, 0))
    matrix = rotate(matrix, math.radians(camera1.getYaw()), (0, 1, 0))

    negativeCameraPos = (-cameraPos[0], -cameraPos[1], -cameraPos[2])
    matrix = translate(matrix, negativeCameraPos)
    
    return matrix
