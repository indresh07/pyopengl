import math

from models import rawModel, modelTexture

class terrain:
    
    def __init__(self, gridX, gridZ, vertexCount, loader, texturePack, blendMap):
        self.size = 256
        self.gridX = gridX * self.size
        self.gridZ = gridZ * self.size
        self.texturePack = texturePack
        self.blendMap = blendMap
        self.vertexCount = vertexCount
        self.terrainModel = self.generateTerrain(loader)

    def getGridX(self):
        return self.gridX

    def getGridZ(self):
        return self.gridZ

    def getTerrainModel(self):
        return self.terrainModel

    def getTexturePack(self):
        return self.texturePack

    def getBlendMap(self):
        return self.blendMap

    def generateTerrain(self, loader):
	count = pow(self.vertexCount, 2)
	vertices = []
	normals = []
	textureCoords = []
	indices = []
	for i in range(self.vertexCount):
	    for j in range(self.vertexCount):
		vertices.append( j/(self.vertexCount - 1) * self.size)
		vertices.append( 0)
		vertices.append( i/(self.vertexCount - 1) * self.size)
		normals.append( 0)
		normals.append( 1)
		normals.append( 0)
		textureCoords.append( j/(self.vertexCount - 1))
		textureCoords.append( i/(self.vertexCount - 1))
    
	for gz in range(self.size - 1):
	    for gx in range(self.size - 1):
		topLeft = (gz*self.size)+gx
		topRight = topLeft + 1
		bottomLeft = ((gz+1)*self.size)+gx
		bottomRight = bottomLeft + 1
		indices.append( topLeft)
                indices.append( bottomLeft)
		indices.append( topRight)
		indices.append( topRight)
		indices.append( bottomLeft)
		indices.append( bottomRight)
    
        return loader.loadVAO(vertices, textureCoords, normals, indices)
        
class entity:

    def __init__(self, model, position, angle, scale):
        self.model = model
        self.position = position
        self.angle= angle
        self.scale = scale

    def setModel(self, model):
        self.model = model

    def setPosition(self, position):
        self.position = position

    def setAngle(self, angle):
        self.angle = angle

    def setScale(self, scale):
        self.scale = scale

    def getModel(self):
        return self.model

    def getPosition(self):
        return self.position

    def getAngle(self):
        return self.angle

    def getScale(self):
        return self.scale

    def getRotation(self):
        return self.angle

    def increasePosition(self, dx, dy, dz):
        self.position[0] += dx
        self.position[1] += dy
        self.position[2] += dz

    def increaseRotation(self, dx, dy, dz):
        self.angle[0] += dx
        self.angle[1] += dy
        self.angle[2] += dz
