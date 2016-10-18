'''get coin working'''
import pygame, sys
from pygame.locals import *
from random import randint

# Creates the screen to draw on
pygame.init()
window = pygame.display.set_mode((1920,1080),pygame.FULLSCREEN)

# Allows a key that is held down to count as multiple presses
pygame.key.set_repeat(1,1)

# Colors the screen white
red=randint(0,255)
green=randint(0,255)
blue=randint(0,255)
def windowFill(red,green,blue):
    window.fill((red,green,blue))
windowFill(255,255,255)

#Initialize game variables
HP=100
coins=0
speed=3
coinOnScreen=False
img = pygame.image.load("dude.gif")
guyX=randint(0,1870)
guyY=randint(0,1030)

# Event Loop
while True:
    
    windowFill(red,green,blue)

    #Show Coins and HP
    font = pygame.font.Font(None, 48)
    text = font.render("COINS: "+str(coins), 1, (0, 0, 0))
    textpos = text.get_rect()
    textpos.centerx = 970
    textpos.centery = 20
    window.blit(text, textpos)

    text = font.render("HP: "+str(HP), 1, (0, 0, 0))
    textpos = text.get_rect()
    textpos.centerx = 970
    textpos.centery = 50
    window.blit(text, textpos)


    #Make Coin
    if not(coinOnScreen) and randint(1,100)==1:
        coinOnScreen=True
        coinX=randint(10,1910)
        coinY=randint(10,1070)

    #Draw Coin
    if coinOnScreen:
        pygame.draw.circle(window, (255,255,0),(coinX,coinY),10,0)

    #Pick up Coin
    '''GET THIS WORKING'''
    if coinOnScreen and guyX-coinX<50 and guyX-coinX>-1 and guyY-coinY>50 and guyY-coinY>-1:
        coinOnScreen=False
        coins+=1
        
    # Draw your person on the screen
    window.blit(img,(guyX,guyY))
    
    # Update the screen
    pygame.display.update()
    
    # Check for key presses and mouse clicks
    for event in pygame.event.get():
        # Determine if the user has closed the window or pressed escape
        if event.type==QUIT or (event.type==KEYUP and event.key==K_ESCAPE):
            # Quit the program
            pygame.quit()
            sys.exit()
        
        # Check if an arrow key is pressed and 
        # move guy in the correct direction
        elif event.type==KEYDOWN:

            if event.key==K_UP: 
                if guyY>1:
                    guyY-=speed

            elif event.key==K_DOWN:
                if guyY<1030:
                    guyY+=speed

            elif event.key==K_LEFT:
                if guyX>1:
                    guyX-=speed

            elif event.key==K_RIGHT:
                if guyX<1870:
                    guyX+=speed

            elif  event.key==K_SPACE:
                red=randint(0,255)
                green=randint(0,255)
                blue=randint(0,255)
                windowFill(red,green,blue)
                
            elif  event.key==K_z and red<255 and green<255 and blue<255:
                red=red+1
                green=green+1
                blue=blue+1
                windowFill(red,green,blue)
                
            elif  event.key==K_x and red>1 and green>1 and blue>1:
                red=red-1
                green=green-1
                blue=blue-1
                windowFill(red,green,blue)
