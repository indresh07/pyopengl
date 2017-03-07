import struct
import numpy

import pygame
from pygame.locals import *

import OpenGL.GL
from OpenGL.GL import *
from OpenGL.GL import shaders

from models import rawModel
from PIL import Image 

class loader:

    vaos = []
    vbos = []
    textures = []

    def loadVAO(self, positions, textureCoords, normals, indices):
        glColor(0, 0, 0)
        vaoID = self.createVAO()
        self.bindIndices(indices)
        self.storeDataInVAO(0, 3, positions)
        self.storeDataInVAO(1, 2, textureCoords)
        self.storeDataInVAO(2, 3, normals)
        self.unbindVAO()
        return rawModel(vaoID, len(indices))
        

    def createVAO(self):
        vaoID = glGenVertexArrays(1)
        self.vaos.append(vaoID)
        glBindVertexArray(vaoID)
        return vaoID

    def loadTexture(self, filename):
        texture = Image.open("res/" + filename + ".png")
        textureData = numpy.array(list(texture.getdata()), numpy.uint32)
        textureID = glGenTextures(1)
        self.textures.append(textureID)
        glBindTexture(GL_TEXTURE_2D, textureID)
        #filters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture.size[0], texture.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        glBindTexture(GL_TEXTURE_2D, 0)
        return textureID


    def storeDataInVAO(self, attributeNo, size, data):
        vboID = glGenBuffers(1)
        self.vbos.append(vboID)
        glBindBuffer(GL_ARRAY_BUFFER, vboID)
        glEnableVertexAttribArray(attributeNo)
        glVertexAttribPointer(attributeNo, size, GL_FLOAT, GL_FALSE, 0, None)
        glBufferData(GL_ARRAY_BUFFER, 4 * len(data), self.storeDataInBuffer(data), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def bindIndices(self, indices):
        vboID = glGenBuffers(1)
        self.vbos.append(vboID)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vboID)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 4 * len(indices), self.storeDataInIntBuffer(indices), GL_STATIC_DRAW)
        
    def unbindVAO(self):
        glBindVertexArray(0)

    def storeDataInIntBuffer(self, data):
        return numpy.array(data, dtype=numpy.uint32)


    def storeDataInBuffer(self, data):
        return numpy.array(data, dtype=numpy.float32)

    def cleanUp(self):
        glDeleteBuffers(len(self.vbos), self.vbos)
        glDeleteVertexArrays(len(self.vaos), self.vaos)
        glDeleteTextures(len(self.textures), self.textures)

class Shaders:

    filePath = "shaders/"
    
    def __init__(self, VSFilename, FSFilename):
        self.VSFilename = VSFilename
        self.FSFilename = FSFilename

    def loadShaderToStringBuffer(self):

        vertexShaderFile = open(self.filePath + self.VSFilename, "r")
        fragmentShaderFile = open(self.filePath + self.FSFilename, "r")

        self.vertexShaderBuffer = vertexShaderFile.read()
        self.fragmentShaderBuffer = fragmentShaderFile.read()

        vertexShaderFile.close()
        fragmentShaderFile.close()
        
    def compile(self):

        self.vertexShader = shaders.compileShader(self.vertexShaderBuffer, GL_VERTEX_SHADER)
        self.fragmentShader = shaders.compileShader(self.fragmentShaderBuffer, GL_FRAGMENT_SHADER)

        self.shaderID = shaders.compileProgram(self.vertexShader, self.fragmentShader)
        return self.shaderID

    def loadFloat(self, name, data):
        glUniform1f(glGetUniformLocation(self.shaderID, name), data)

    def loadVector3f(self, name, data):
        glUniform3f(glGetUniformLocation(self.shaderID, name), data[0], data[1], data[2])

    def loadInt(self, name, data):
        glUniform1i(glGetUniformLocation(self.shaderID, name), data)
        
    def loadMatrix(self, name, data):

        matrix = numpy.array(data, numpy.float32)
        glUniformMatrix4fv(glGetUniformLocation(self.shaderID, name), 1, GL_FALSE, matrix)

    def cleanUp(self):
        glDeleteShader(self.vertexShader)
        glDeleteShader(self.fragmentShader)
        glDetachShader(self.shaderID, self.vertexShader)
        glDetachShader(self.shaderID, self.fragmentShader)
        glDeleteProgram(self.shaderID)

class ModelLoader:

    vertices = []
    textures = []
    normals = []
    indices = []
    textureArray = {}
    normalsArray = {}
    texturesList = []
    normalsList = []

    def loadModel(self, filename, loader):

        dModel = open("res/" + filename + ".obj", "r")
            
        line = ""
        while(True):
            line = dModel.readline()
            
            currentLine = line.split(" ")

            if(line.startswith("v ")):

                self.vertices.append(float(currentLine[1]))
                self.vertices.append(float(currentLine[2]))
                self.vertices.append(float(currentLine[3]))

            elif(line.startswith("vt ")):

                texture = (float(currentLine[1]), float(currentLine[2]))
                self.textures.append(texture)

            elif(line.startswith("vn ")):

                normal = (float(currentLine[1]), float(currentLine[2]), float(currentLine[3]))
                self.normals.append(normal)

            elif(line.startswith("f ")):
                break
            
        while(line is not ""):
    
            if(line.startswith("f ") == False):
                line = dModel.readline()
                continue

            currentLine = line.split(" ")
            vertex1 = currentLine[1].split("/")
            vertex2 = currentLine[2].split("/")
            vertex3 = currentLine[3].split("/")

            self.processVertex(vertex1)
            self.processVertex(vertex2)
            self.processVertex(vertex3)

            line = dModel.readline()

        for i in range(len(self.textureArray)):
            self.texturesList.append(self.textureArray[i])

        for i in range(len(self.textureArray)):
            self.normalsList.append(self.normalsArray[i])
                
        return loader.loadVAO(self.vertices, self.texturesList, self.normalsList, self.indices)


    def processVertex(self, vertexData):
        currentVertexPointer = (int(float(vertexData[0]))) - 1
        self.indices.append(currentVertexPointer)

        currentTexture = self.textures[(int(float(vertexData[1]))) - 1]
        self.textureArray[currentVertexPointer*2] = currentTexture[0]
        self.textureArray[currentVertexPointer*2 + 1] = 1 - currentTexture[1]

        currentNormal = self.normals[(int(float(vertexData[2]))) - 1]
        self.normalsArray[currentVertexPointer*3] = currentNormal[0]
        self.normalsArray[currentVertexPointer*3 + 1] = currentNormal[1]
        self.normalsArray[currentVertexPointer*3 + 2] = currentNormal[2]

    def cleanUp(self):
        del self.vertices[:]
        del self.textures[:]
        del self.normals[:]
        del self.indices[:]
        self.textureArray.clear()
        self.normalsArray.clear()
        del self.texturesList[:]
        del self.normalsList[:]

        
        
        
            
            

            


        
        
        
