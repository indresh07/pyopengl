import maths

import OpenGL.GL
from OpenGL.GL import *

from models import rawModel, terrainTexture
from sprites import *
from loader import Shaders
from lights import *

class masterRenderer:

    def __init__(self, entityShader, terrainShader):
        self.entityShader = entityShader
        self.terrainShader = terrainShader
        self.entities = {}
        self.terrains = []

    def prepare(self):
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glClearColor(0.5, 0.5, 0.5, 1)
        glColor(1, 1, 1, 1 )
        self.entityRender = entityRenderer()
        self.terrainRender = terrainRenderer()

    def loadProjectionMatrix(self, shader):
        projectionMatrix = maths.projectionMatrix(800/600.0, 70, 0.1, 1000)
        shader.loadMatrix("projectionMatrix", projectionMatrix)
        
    def loadViewMatrix(self, shader, camera):
        viewMatrix = maths.viewMatrix(camera)
        shader.loadMatrix("viewMatrix", viewMatrix)

    def renderer(self, entityProgramID, terrainProgramID, sun, camera):
        self.prepare()
        glUseProgram(entityProgramID)
        self.loadProjectionMatrix(self.entityShader)
        self.loadViewMatrix(self.entityShader, camera)
        self.entityShader.loadVector3f("lightPosition", sun.getPosition())
        self.entityShader.loadVector3f("lightColor", sun.getColor())
        self.entityRender.render(self.entityShader, self.entities)
        glUseProgram(0)

        glUseProgram(terrainProgramID)
        self.loadProjectionMatrix(self.terrainShader)
        self.loadViewMatrix(self.terrainShader, camera)
        self.terrainShader.loadVector3f("lightPosition", sun.getPosition())
        self.terrainShader.loadVector3f("lightColor", sun.getColor())
        self.terrainShader.loadInt("backgroundTexture", 0)
        self.terrainShader.loadInt("rTexture", 1)
        self.terrainShader.loadInt("gTexture", 2)
        self.terrainShader.loadInt("bTexture", 3)
        self.terrainShader.loadInt("blendMap", 4)
        self.terrainRender.renderTerrain(self.terrainShader, self.terrains)
        glUseProgram(0)

        self.cleanUp()

    def processEntity(self, model, entities):
        self.entities[model] = entities

    def processTerrain(self, terrain):
        self.terrains.append(terrain)
        
    def cleanUp(self):
        del self.terrains[:]
        self.entities.clear()


class entityRenderer:

    def __init__(self):
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

    def enableCulling(self):
        glEnable(GL_CULL_FACE)

    def disableCulling(self):
        glDisable(GL_CULL_FACE)

    def render(self, shader, entities):
        if(entities.keys() != []):
            for model in entities.keys():
                self.prepareTexturedModel(shader, model)
                batch = entities[model]
                for entity in batch:
                    self.prepareInstance(shader, entity)
                    glDrawElements(GL_TRIANGLES, model.getRawModel().getNVertex(), GL_UNSIGNED_INT, None)
                self.unbindTexturedModel()
            entities.clear()
        else:
            print "No texture to load"
            
    def prepareTexturedModel(self, shader, texturedModel):
        model = texturedModel.getRawModel()
        texture = texturedModel.getTexture()
        shader.loadFloat("reflectivity" , texture.getReflectivity())
        shader.loadFloat("shineDampness" , texture.getShineDampness())
        if(texture.useFakeLight()):
            shader.loadFloat("fakeLight", 1)
        else:
            shader.loadFloat("fakeLight", 0)
        glBindVertexArray(model.getVaoID())
        if(texture.isTransparent()):
            self.disableCulling()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texturedModel.getTexture().getID())

    def unbindTexturedModel(self):
        self.enableCulling()
        glBindVertexArray(0)
        glBindTexture(GL_TEXTURE_2D, 0)

    def prepareInstance(self, shader, entity):
        transformationMatrix = maths.transformationMatrix(entity.getPosition(), entity.getRotation(), entity.getScale())
        shader.loadMatrix("transformationMatrix", transformationMatrix)

class terrainRenderer:

    def renderTerrain(self, shader, terrains):
        for terrain in terrains:
            self.prepareTerrain(shader, terrain)
            self.prepareTerrainInstance(shader, terrain)
            glDrawElements(GL_TRIANGLES, terrain.getTerrainModel().getNVertex(), GL_UNSIGNED_INT, None)
            self.unbindTerrain()
        
    
    def prepareTerrain(self, shader, terrain):
        model = terrain.getTerrainModel()
        self.bindTextures(terrain)
        shader.loadFloat("reflectivity" , 0)
        shader.loadFloat("shineDampness" , 1)
        glBindVertexArray(model.getVaoID())

    def bindTextures(self, terrain):
        texturePack = terrain.getTexturePack()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texturePack.getBackgroundTexture())
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, texturePack.getRTexture())
        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_2D, texturePack.getGTexture())
        glActiveTexture(GL_TEXTURE3)
        glBindTexture(GL_TEXTURE_2D, texturePack.getBTexture())
        glActiveTexture(GL_TEXTURE4)
        glBindTexture(GL_TEXTURE_2D, terrain.getBlendMap())
        
    def unbindTerrain(self):
        glBindVertexArray(0)
        glBindTexture(GL_TEXTURE_2D, 0)

    def prepareTerrainInstance(self, shader, terrain):
        transformationMatrix = maths.transformationMatrix([terrain.getGridX(), 0, terrain.getGridZ()],[0, 0, 0], 1)
        shader.loadMatrix("transformationMatrix", transformationMatrix)

        
