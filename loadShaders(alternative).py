import OpenGL.GL
from OpenGL.GL import shaders
from OpenGL.GL import *

class Shaders:

    filePath = "shaders/"
    
    def __init__(self, VSFilename, FSFilename):
        self.VSFilename = VSFilename
        self.FSFilename = FSFilename

    def loadShaderToStringBuffer(self):

        vertexShaderFile = open(self.filePath + self.VSFilename, "r")
        fragmentShaderFile = open(self.filePath + self.FSFilename, "r")

        self.vertexShaderBuffer = vertexShaderFile.read(1000).rstrip("\n")
        self.fragmentShaderBuffer = fragmentShaderFile.read(1000).rstrip("\n")

        print self.vertexShaderBuffer
        print self.fragmentShaderBuffer

        vertexShaderFile.close()
        fragmentShaderFile.close()

    def compile(self):

        vertexShader = shaders.compileShader(self.vertexShaderBuffer, GL_VERTEX_SHADER)
        fragmentShader = shaders.compileShader(self.fragmentShaderBuffer, GL_FRAGMENT_SHADER)

        return shaders.compileProgram(vertexShader, fragmentShader)

