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

#Define Methods
def windowFill(red,green,blue):
    window.fill((red,green,blue))
def drawText(text,centerX,centerY):
    textpos = text.get_rect()
    textpos.centerx = centerX
    textpos.centery = centerY
    window.blit(text, textpos)

#Initialize everything
font=pygame.font.Font(None, 48)
HP=100
coins=0
speed=1
coinOnScreen=False
img = pygame.image.load("dude.gif")
guyX=randint(0,1870)
guyY=randint(0,1030)
red=0
green=0
blue=0

#Enemy Stuff
enemy1img=pygame.image.load("enemy1.gif")
#[IMAGE, HP, SPEED, damage per loop (small, display of health is rounded)]
#enemy1=[enemy1img, 10, 2, 0.01]
enemyOnScreen=False
enemyType=None

# Event Loop
while True:
    
    windowFill(red,green,blue)
    pygame.draw.rect(window, (50,50,50), (0,0,100,50),0)
    font=pygame.font.Font(None, 27)
    drawText(font.render("+ SPEED: 1", 1, (255, 0, 0)),50,25)
    font=pygame.font.Font(None, 48)
    

    #Show Coins and HP
    drawText(font.render("COINS: "+str(coins), 1, (255,255,0)),970,20)
    drawText(font.render("HP: "+str(int(HP//1)), 1, ((0+2.5*(100-HP))//1, (255-2.5*(100-HP))//1, 0)),970,50)

    #Make Coin
    if not(coinOnScreen) and randint(1,500)==1:
        coinOnScreen=True
        coinX=randint(10,1910)
        coinY=randint(10,1070)

    #Draw Coin
    if coinOnScreen:
        pygame.draw.circle(window, (255,255,0),(coinX,coinY),8,0)

    #Pick up Coin
    if coinOnScreen and coinX-guyX<60 and coinX-guyX>-5 and guyY-coinY>-60 and guyY-coinY<10:
        coinOnScreen=False
        coins+=1

    #Make Enemy
    if not(enemyOnScreen) and randint(1,1000)==1:
        enemyOnScreen=True
        enemyType=1
        enemyX=randint(0,1888)
        enemyY=randint(0,1048)

    if enemyOnScreen and enemyType==1:
        if enemyX<guyX:
            enemyX+=1
        if enemyX>guyX:
            enemyX-=1
        if enemyY<guyY:
            enemyY+=1
        if enemyY>guyY:
            enemyY-=1


        window.blit(enemy1img, (enemyX, enemyY))

    if enemyOnScreen and enemyType==1 and enemyX-guyX<48 and enemyX-guyX>-32 and guyY-enemyY>-48 and guyY-enemyY<32:
        HP-=0.01
    



        
        
    # Draw your person on the screen
    window.blit(img,(guyX,guyY))
    
    # Update the screen
    pygame.display.update()

    if HP<=0:
        pygame.quit()
        sys.exit()
    # Check for key presses
    for event in pygame.event.get():
        if (event.type==KEYUP and event.key==K_ESCAPE):
            pygame.quit()
            sys.exit()
        
        # Check if an arrow key is pressed and 
        # move guy in the correct direction
        elif event.type==KEYDOWN:

            if event.key==K_UP: 
                if guyY>1:
                    guyY-=speed

            elif event.key==K_DOWN:
                if guyY<1032:
                    guyY+=speed

            elif event.key==K_LEFT:
                if guyX>1:
                    guyX-=speed

            elif event.key==K_RIGHT:
                if guyX<1875:
                    guyX+=speed
                    
            elif event.key==K_1:
                if coins<speed*speed*speed:
                    drawText(font.render("NOT ENOUGH COINS! Cost: "+str(speed*speed*speed), 1, (255, 127,0)),970,1000)
                    pygame.display.update()
                        
                elif speed==6:
                    drawText(font.render("ALREADY AT MAXIMUM VELOCITY!", 1, (255, 0, 0)),970,1000)
                    pygame.display.update()
                        
                else:
                    drawText(font.render("Confirm Purchase \"SPEED +1\" for "+str(speed*speed)+" Coins? Y/N", 1, (255, 255, 0)),970,1000)
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type==KEYDOWN:
                            while not(event.type==KEYDOWN and (event.key==K_y or event.key==K_n)):
                                for event in pygame.event.get():
                                    if event.type==KEYDOWN:
                                        if event.key==K_y:
                                            coins-=speed*speed
                                            speed+=1
                                        elif event.key==K_n:
                                            break
