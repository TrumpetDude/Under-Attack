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
regenSpeed=0.001
coinOnScreen=False
dude = pygame.image.load("dude.gif")
dudeDamaged = pygame.image.load("dudeDamaged.gif")
guyX=randint(0,1870)
guyY=randint(0,1030)
red=0
green=0
blue=0
HPr=0
HPg=255
pygame.mouse.set_visible(False)

#Enemy Stuff
enemy1=pygame.image.load("enemy1.gif")
enemy1damaged=pygame.image.load("enemy1damaged.gif")
#[IMAGE, HP, SPEED, damage per loop (small, display of health is rounded)]
#enemy1=[10, 2, 0.05]
enemy1OnScreen=False

# Event Loop
while True:

    #Draw background and words
    windowFill(red,green,blue)
    pygame.draw.rect(window, (50,50,50), (0,0,250,50),0)
    pygame.draw.line(window,(0,0,0) ,(105,0), (105,50), 5)
    font=pygame.font.Font(None, 27)
    drawText(font.render("+ SPEED: 1", 1, (255, 0, 0)),50,25)
    drawText(font.render("+ HP REGEN: 2", 1, (255, 0, 0)),175,25)
    font=pygame.font.Font(None, 48)
    drawText(font.render("COINS: "+str(coins), 1, (255,255,0)),970,20)
    drawText(font.render("HP: "+str(int(HP//1)), 1, (HPr, HPg, 0)),970,50)
    if enemy1OnScreen:
        drawText(font.render("TOTAL ENEMY HP: "+str(int(enemy1HP//1)), 1, (255,0,0)),970,80)
        
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

    #Make Enemy1
    if not(enemy1OnScreen) and randint(1,500)==1:
        enemy1OnScreen=True
        enemy1X=randint(0,1888)
        enemy1Y=randint(0,1048)
        enemy1HP=10


    #Draw person on the screen
    window.blit(dude,(guyX,guyY))

    #Take damage from enemy 1
    if enemy1OnScreen and enemy1X-guyX<48 and enemy1X-guyX>-32 and guyY-enemy1Y>-48 and guyY-enemy1Y<32:
        HP-=0.05
        window.blit(dudeDamaged,(guyX,guyY))
    if HP>=50:
        HPr=0+5*(100-HP)
    else:
        HPr=255
        
    if HPr==255:
        HPg=255-5*(50-HP)

    

    #Move and draw enemy1
    if enemy1OnScreen:
        if enemy1X<guyX:
            enemy1X+=1
        if enemy1X>guyX:
            enemy1X-=1
        if enemy1Y<guyY:
            enemy1Y+=1
        if enemy1Y>guyY:
            enemy1Y-=1
        window.blit(enemy1, (enemy1X, enemy1Y))

    #Kill enemy1
    if enemy1OnScreen and enemy1HP<=0:
        enemy1OnScreen=False
        coins+=10
    #Regen HP
    if HP<100-regenSpeed:
        HP+=regenSpeed
    elif HP<100:
        HP=100
    
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
                    drawText(font.render("Confirm Purchase \"SPEED +1\" for "+str(speed*speed*speed)+" Coins? ENTER/BACKSPACE", 1, (255, 255, 0)),970,1000)
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type==KEYDOWN:
                            while not(event.type==KEYDOWN and (event.key==K_RETURN or event.key==K_BACKSPACE)):
                                for event in pygame.event.get():
                                    if event.type==KEYDOWN:
                                        if event.key==K_RETURN:
                                            coins-=speed*speed*speed
                                            speed+=1
                                        elif event.key==K_BACKSPACE:
                                            break

            elif event.key==K_2:
                if coins<int(1000*regenSpeed*1000*regenSpeed*1000*regenSpeed):
                    drawText(font.render("NOT ENOUGH COINS! Cost: "+str(int(1000*regenSpeed*1000*regenSpeed*1000*regenSpeed)), 1, (255, 127,0)),970,1000)
                    pygame.display.update()
                        
                elif regenSpeed==0.006:
                    drawText(font.render("ALREADY AT MAXIMUM HP REGEN SPEED!", 1, (255, 0, 0)),970,1000)
                    pygame.display.update()
                        
                else:
                    drawText(font.render("Confirm Purchase \"HP REGEN SPEED +1\" for "+str(int(1000*regenSpeed*1000*regenSpeed*1000*regenSpeed))+" Coins? ENTER/BACKSPACE", 1, (255, 255, 0)),970,1000)
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type==KEYDOWN:
                            while not(event.type==KEYDOWN and (event.key==K_RETURN or event.key==K_BACKSPACE)):
                                for event in pygame.event.get():
                                    if event.type==KEYDOWN:
                                        if event.key==K_RETURN:
                                            coins-=int(1000*regenSpeed*1000*regenSpeed*1000*regenSpeed)
                                            regenSpeed+=0.001
                                        elif event.key==K_BACKSPACE:
                                            break

        elif event.type==KEYUP:
            if event.key==K_SPACE:
                if enemy1OnScreen and enemy1X-guyX<48 and enemy1X-guyX>-32 and guyY-enemy1Y>-48 and guyY-enemy1Y<32:
                    enemy1HP-=1
                    window.blit(enemy1damaged, (enemy1X,enemy1Y))
                    pygame.display.update()
                    pygame.time.delay(100)
