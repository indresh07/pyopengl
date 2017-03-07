import pygame
from pygame.locals import *

import OpenGL.GL
from OpenGL.GL import *
from OpenGL.GLU import *

import random

from models import *
from loader import *
from renderer import *
from camera import *
from sprites import *
from lights import *

class game:

    def __init__(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        pygame.init()
        pygame.display.set_mode((self.screenWidth, self.screenHeight), DOUBLEBUF|OPENGL)

    def init(self):
        self.load = loader()
        self.light = lights([200, 200, -100], [1, 1, 1])
        self.entityShader = Shaders("vertexShader.vs", "fragmentShader.fs")
        self.terrainShader = Shaders("TerrainVertexShader.vs", "TerrainFragmentShader.fs")
        self.rend = masterRenderer(self.entityShader, self.terrainShader)
        self.entityShader.loadShaderToStringBuffer()
        self.terrainShader.loadShaderToStringBuffer()
        self.camera1 = camera(numpy.array([0, 0, 0], numpy.float32), 10, 0, 0)
        
        self.entityProgramID = self.entityShader.compile()
        self.terrainProgramID = self.terrainShader.compile()
        
        self.trees = self.loadModels(self.load, "tree", "treetex", 4, 1, 0, False, False)
        self.grass = self.loadModels(self.load, "grassModel", "grassTexture", 3, 1, 0, True, True)
        self.ferns = self.loadModels(self.load, "fern", "fern", 2, 1, 0, True, True)
        self.dragons = self.loadModels(self.load, "dragon", "DragonBlender", 1, 5, 5, False, False)

        
        dModel = ModelLoader()
        model1 = dModel.loadModel("player", self.load)
        texture = modelTexture(self.load.loadTexture("player"), 10,100, transparent, fakeLight)
        textureModel = texturedModel(model1, texture)
        self.player = [entity(textureModel, numpy.array([x, height, z], numpy.float32), numpy.array([0, 0, -5], numpy.float32), 1)]
        backgroundTexture = self.load.loadTexture("grassy")
        rTexture = self.load.loadTexture("dirt")
        gTexture = self.load.loadTexture("mud")
        bTexture = self.load.loadTexture("path")
        blendMap = self.load.loadTexture("blendMap")
        texturePack = terrainTexture(backgroundTexture, rTexture, gTexture, bTexture)        
        
        self.terrain1 = terrain(-0.5, -0.5, 128, self.load, texturePack, blendMap)
        
        glTranslate(0, 0, 0)
        
        
    def loadModels(self, load, objectFile, textureFile, scale, count, height, transparent, fakeLight):
        objects = []
        dModel = ModelLoader()
        
        model1 = dModel.loadModel(objectFile, load)
        texture = modelTexture(load.loadTexture(textureFile), 10,100, transparent, fakeLight)
        textureModel = texturedModel(model1, texture)

        limit = round(100/scale)

        for i in range(count):
            x = random.randrange(-limit, limit, 2)
            z = random.randrange(-limit, limit, 2)
            objects.append(entity(textureModel, numpy.array([x, height, z], numpy.float32), numpy.array([0, 0, 0], numpy.float32), scale))
            if(objectFile == "grassModel"):
                objects.append(entity(textureModel, numpy.array([x, height, z], numpy.float32), numpy.array([0, 90, 0], numpy.float32), scale))

        dModel.cleanUp()
        return objects

        
    def create(self):
        self.init()
        self.gameloop()
        

    def gameloop(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick()
            self.camera1.readInput()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    load.cleanUp()
                    self.entityShader.cleanUp()
                    self.terrainShader.cleanUp()
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.load.cleanUp()
                        self.entityShader.cleanUp()
                        self.terrainShader.cleanUp()
                        pygame.quit()
                        return

            self.camera1.move()

            self.rend.processEntity(self.trees[0].getModel(), self.trees)
            self.rend.processEntity(self.ferns[0].getModel(), self.ferns)
            self.rend.processEntity(self.grass[0].getModel(), self.grass)
            self.rend.processEntity(self.dragons[0].getModel(), self.dragons)
            self.rend.processEntity(self.player[0].getModel(), self.player)
            
            self.rend.processTerrain(self.terrain1)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            self.rend.renderer(self.entityProgramID, self.terrainProgramID, self.light, self.camera1)
            pygame.display.flip()
            print "FPS : " + str(round(clock.get_fps()))
