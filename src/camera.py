import pygame
from pygame.locals import *

class camera:

    def __init__(self, position, pitch, yaw, roll):
        self.position = position
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll
        
    def readInput(self):
        self.keyboard = pygame.key.get_pressed()
        return self.keyboard

    def move(self):

        if(self.keyboard[pygame.K_UP] == True):
            self.position[2] -= 0.1

        if(self.keyboard[pygame.K_DOWN] == True):
            self.position[2] += 0.1

        if(self.keyboard[pygame.K_LEFT] == True):
            self.position[0] -= 0.01

        if(self.keyboard[pygame.K_RIGHT] == True):
            self.position[0] += 0.01

        if(self.keyboard[pygame.K_9] == True):
            self.position[1] -= 0.01

        if(self.keyboard[pygame.K_0] == True):
            self.position[1] += 0.01

        if(self.keyboard[pygame.K_s] == True):
            if(self.pitch == 0):
                self.pitch = 359
            else:
                self.pitch -= 1

        if(self.keyboard[pygame.K_w] == True):
            if(self.pitch == 360):
                self.pitch = 1
            else:
                self.pitch += 1

        if(self.keyboard[pygame.K_d] == True):
            if(self.yaw == 0):
                self.yaw = 359
            else:
                self.yaw -= 1

        if(self.keyboard[pygame.K_a] == True):
            if(self.yaw == 360):
                self.yaw = 1
            else:
                self.yaw += 1


        
        

    def getPosition(self):
        return self.position

    def getPitch(self):
        return self.pitch

    def getYaw(self):
        return self.yaw

    def getRoll(self):
        return self.roll
