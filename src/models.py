class terrainTexture:

    def __init__(self, backgroundTexture, rTexture, gTexture, bTexture):
        self.backgroundTexture = backgroundTexture
        self.rTexture = rTexture
        self.gTexture = gTexture
        self.bTexture = bTexture

    def getBackgroundTexture(self):
        return self.backgroundTexture

    def getRTexture(self):
        return self.rTexture
    
    def getGTexture(self):
        return self.gTexture
    
    def getBTexture(self):
        return self.bTexture


class texturedModel:

    def __init__(self, rawModel, texture):
        self.rawModel = rawModel
        self.texture = texture

    def getRawModel(self):
        return self.rawModel

    def getTexture(self):
        return self.texture

class modelTexture:

    def __init__(self, id, reflectivity, shineDampness, transparent, fakeLight):
        self.id = id
        self.reflectivity = reflectivity
        self.shineDampness = shineDampness
        self.transparent = transparent
        self.fakeLight = fakeLight

    def getID(self):
        return self.id

    def isTransparent(self):
        return self.transparent

    def useFakeLight(self):
        return self.fakeLight

    def getReflectivity(self):
        return self.reflectivity

    def getShineDampness(self):
        return self.shineDampness

    def setReflectivity(self, reflectivity):
        self.reflectivity = reflectivity

    def setShineDampness(self, shineDampness):
        self.shineDampness = shineDampness

class rawModel:

    def __init__(self, vaoID, nVertex):
        self.vaoID = vaoID
        self.nVertex = nVertex

    def getVaoID(self):
        return self.vaoID

    def getNVertex(self):
        return self.nVertex
