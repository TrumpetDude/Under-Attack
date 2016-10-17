'''
Johnny Dollard
Period 4
"ifs" Lab 4
'''
import pygame
from pygame.locals import *
from random import randint


# Create a class called Person
class Person:
    
    # Create a constructor method that sets self.x to newX, 
    # self.y to newY and loads the image "dude.gif" into self.img
    def __init__ (self,newX,newY):
        self.x=newX
        self.y=newY
        self.img = pygame.image.load("dude.gif")
    
    # draw the image on the surface
    def draw(self, window):
        window.blit(self.img,(self.x,self.y))
    
    def moveLeft(self, speed):
        # Change x so that the object can move left
        if self.x>1:
            self.x-=speed
        return self.x
    

    def moveRight(self, speed):
        # Change x so that the object can move right
        myRec = self.getRec()
        width = myRec[2]
        if self.x<1920-myRec[2]:
            self.x+=speed
        return self.x
    
       

    def moveUp(self, speed):
        # Change y so that the object can move up
        if self.y>1:
            self.y-=speed
        return self.y
    

    
    def moveDown(self, speed):
        # Change y so that the object can move down
        myRec = self.getRec()
        height = myRec[3]
        if self.y<1080-myRec[3]:
            self.y+=speed
        return self.y

    def getCoord(self):
        guyX=self.x
        guyY=self.y
        return (self.x, self.y, guyX, guyY)
    
    def getRec(self):
        myRec = self.img.get_rect()
        return (self.x, self.y, myRec[2], myRec[3])
