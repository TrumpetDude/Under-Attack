#Setup
import pygame, sys
from pygame.locals import *
from random import randint
pygame.init()
window = pygame.display.set_mode((1300,700))
pygame.display.set_caption("Zombie Apocalypse","Zombie Apocalypse")
pygame.key.set_repeat(1,1)
from array import array
from time import sleep
import pygame
from pygame.mixer import Sound, get_init, pre_init
from tone import Note

#Methods
def windowFill(red,green,blue):
    window.fill((red,green,blue))
def drawText(text, size, color, centerX, centerY):
    font=pygame.font.Font("PressStart2P.ttf", size)
    renderedText=font.render(text,True,color)
    textpos=renderedText.get_rect()
    textpos.centerx=centerX
    textpos.centery=centerY
    window.blit(renderedText, textpos)
def playSound(hz,ms):
    pre_init(44100, -16, 1, 1024)
    Note(hz).play(ms)
def done():
    pygame.quit()
    sys.exit(0)
    
#Initialize Variables
ticks=0
HP=100
coins=0
score=0
baseSpeed=1
speedStart=-501
infectStart=-2001
infectAmount=0
regenSpeed=0.001
guyX=randint(0,1250)
guyY=randint(0,650)
red=0
green=0
blue=0
HPr=0
HPg=255
coinOnScreen=False
chestOnScreen=False
doubleSpeedOnScreen=False
plusHealthOnScreen=False
zombies = []

#Load Images
zombie=pygame.image.load("zombie.gif")
chestOpened=pygame.image.load("chestOpened.gif")
dude=pygame.image.load("dude.gif")
dudeDamaged=pygame.image.load("dudeDamaged.gif")
chest=pygame.image.load("chest.gif")
doubleSpeed=pygame.image.load("doubleSpeed.gif")
plusHealth=pygame.image.load("health.gif")



while HP>0:
    ticks+=1
    
    #Draw Background and words
    windowFill(red,green,blue)
    pygame.draw.rect(window, (50,50,50), (0,0,315,50),0)
    pygame.draw.line(window,(0,0,0) ,(125,0), (125,50), 5)
    drawText("+ SPEED: 1",12,(0, 0, 255),50,25)
    drawText("+ HP REGEN: 2",12,(255, 0, 255),220,25)
    drawText("COINS: "+str(coins), 26, (255,255,0),650,20)
    drawText("HP: "+str(int(HP//1)), 26, (HPr, HPg, 0),650,50)
    drawText("SCORE: "+str(score), 26, (255,255,255),1100,20)
    drawText("ZOMBIES: "+str(len(zombies)), 26, (255,0,0),650,80)

    #Make Coin
    if not(coinOnScreen) and randint(1,300)==1:
        coinOnScreen=True
        coinX=randint(10,1290)
        coinY=randint(10,690)
    #Make Chest
    if not(chestOnScreen) and randint(1,6500)==1:
        chestOnScreen=True
        chestX=randint(16,1200)
        chestY=randint(1,639)
    #Make Double Speed
    if not(doubleSpeedOnScreen) and randint(1,600)==1 and ticks-speedStart>500:
        doubleSpeedOnScreen=True
        speedX=randint(0,1267)
        speedY=randint(0,667)
    #Make +Health
    if not(plusHealthOnScreen) and randint(1,1000)==1:
        plusHealthOnScreen=True
        healthX=randint(0,1267)
        healthY=randint(0,667)
    #Make Zombie
    if randint(1,500)==1:
        zombies.append([randint(0,1250),randint(0,650)])
        
    #Draw Coin
    if coinOnScreen:
        pygame.draw.circle(window, (255,255,0),(coinX,coinY),8,0)
    #Draw Chest
    if chestOnScreen:
        window.blit(chest, (chestX, chestY))
    #Draw and Move Double Speed
    if doubleSpeedOnScreen:
        window.blit(doubleSpeed, (speedX, speedY))
        if speedX<1:
            speedX=1
        if speedX>1254:
            speedX=1254
        if speedY<2:
            speedY=2
        if speedY>652:
            speedY=652
        if speedX<=guyX:
            speedX-=1
        elif speedX>=guyX:
            speedX+=1
        if speedY<=guyY:
            speedY-=1
        elif speedY>=guyY:
            speedY+=1
    #Draw and Move +Health
    if plusHealthOnScreen:
        window.blit(plusHealth, (healthX, healthY))
        if healthX<1:
            healthX=1
        if healthX>1254:
            healthX=1254
        if healthY<2:
            healthY=2
        if healthY>652:
            healthY=652
        if healthX<=guyX:
            healthX-=1
        elif healthX>=guyX:
            healthX+=1
        if healthY<=guyY:
            healthY-=1
        elif healthY>=guyY:
            healthY+=1

        
    #Pick up Coin
    if coinOnScreen and coinX-guyX<60 and coinX-guyX>-5 and guyY-coinY>-60 and guyY-coinY<10:
        playSound(220, 50)
        coinOnScreen=False
        coins+=1
        score+=10
        playSound(220, 50)
    #Pick up Double Speed
    if doubleSpeedOnScreen and speedX-guyX<48 and speedX-guyX>-32 and guyY-speedY>-48 and guyY-speedY<32:
        playSound(264, 50)
        doubleSpeedOnScreen=False
        speedStart=ticks
        score+=50
    #Pick up +Health
    if plusHealthOnScreen and healthX-guyX<48 and healthX-guyX>-32 and guyY-healthY>-48 and guyY-healthY<32:
        playSound(293.333333, 50)
        plusHealthOnScreen=False
        score+=50
        HP+=5
        if HP>100:
            HP=100
        infectStart=ticks-2001

    #Take damagefrom infection
    if ticks-infectStart<2000:
        window.blit(dudeDamaged, (guyX,guyY))
        HP-= infectAmount
    else:
        window.blit(dude,(guyX,guyY))
    

    
    #Get Infected by Zombie
    for z in zombies:
        if z[0]-guyX<48 and z[0]-guyX>-48 and guyY-z[1]>-48 and guyY-z[1]<48 and randint(1,100) == 1:
            zombies.pop(0)
            HP-=5
            infectAmount += 0.015
            infectStart=ticks

        
    #Change HP text color
    if HP>=50:
        HPr=0+5*(100-HP)
    else:
        HPr=255
    if HPr==255:
        HPg=255-5*(50-HP)

    #Move and draw Zombies
    for z in zombies:
        if z[0]<guyX:
            z[0]+=randint(1,4)
        elif z[0]>guyX:
            z[0]-=randint(1,4)
        if z[1]<guyY:
            z[1]+=randint(1,4)
        elif z[1]>guyY:
            z[1]-=randint(1,4)
        window.blit(zombie, (z[0], z[1]))


    #Regen HP
    if HP<100-regenSpeed:
        HP+=regenSpeed
    else:
        HP=100

    #Open Chest
    if chestOnScreen and chestX-guyX<48 and chestX-guyX>-100 and guyY-chestY>-48 and guyY-chestY<60:
        playSound(165, 50)
        chestOnScreen=False
        window.blit(chestOpened, (chestX-15,chestY))
        pygame.display.update()
        coins+=randint(10,50)
        score+=10*randint(10,100)
        pygame.time.delay(500)
        
    # Update the screen
    pygame.display.update()
        
    # Check for key presses
    for event in pygame.event.get():
        if (event.type==KEYUP and event.key==K_ESCAPE)or event.type==QUIT:
            done()
        
        # Check if an arrow key is pressed and 
        # move guy in the correct direction
        elif event.type==KEYDOWN:
            if ticks-speedStart<500:
                speed=baseSpeed*2
            else:
                speed=baseSpeed

            if event.key==K_w:
                if guyY>1:
                    guyY-=speed

            elif event.key==K_s:
                if guyY<652:
                    guyY+=speed

            elif event.key==K_a:
                if guyX>1:
                    guyX-=speed

            elif event.key==K_d:
                if guyX<1255:
                    guyX+=speed

            elif event.key==K_EQUALS:#DEVELOPER ONLY!
                coins+=1
                score+=0
                
                    
            elif event.key==K_1:
                if baseSpeed>=5.999:
                    drawText("ALREADY AT MAXIMUM VELOCITY!", 24, (255, 0, 0),650,680)
                    pygame.display.update()

                elif coins<baseSpeed*baseSpeed*baseSpeed:
                    drawText("NOT ENOUGH COINS! Cost: "+str(baseSpeed*baseSpeed*baseSpeed), 24, (255, 127,0),650,680)
                    pygame.display.update()
                        
                else:
                    drawText("Confirm Purchase \"SPEED +1\" for "+str(baseSpeed*baseSpeed*baseSpeed)+" Coins? ENTER/BACKSPACE", 20, (0, 0, 255),650,680)
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type==KEYDOWN:
                            while not(event.type==KEYDOWN and (event.key==K_RETURN or event.key==K_BACKSPACE)):
                                for event in pygame.event.get():
                                    if event.type==KEYDOWN:
                                        if event.key==K_RETURN:
                                            playSound(206.25, 50)
                                            coins-=baseSpeed*baseSpeed*baseSpeed
                                            baseSpeed+=1
                                        elif event.key==K_BACKSPACE:
                                            break

            elif event.key==K_2:                       
                if regenSpeed>=0.005999:
                    drawText("ALREADY AT MAXIMUM HP REGEN SPEED!", 24, (255, 0, 0),650,680)
                    pygame.display.update()

                elif coins<int(1000*regenSpeed*1000*regenSpeed*1000*regenSpeed):
                    drawText("NOT ENOUGH COINS! Cost: "+str(int(1000*regenSpeed*1000*regenSpeed*1000*regenSpeed)), 24, (255, 127,0),650,680)
                    pygame.display.update()
                    
                else:
                    drawText("Confirm Purchase \"HP REGEN SPEED +1\" for "+str(int(1000*regenSpeed*1000*regenSpeed*1000*regenSpeed))+" Coins? RETURN/BACKSPACE", 19, (255, 0, 255),650,680)
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type==KEYDOWN:
                            while not(event.type==KEYDOWN and (event.key==K_RETURN or event.key==K_BACKSPACE)):
                                for event in pygame.event.get():
                                    if event.type==KEYDOWN:
                                        if event.key==K_RETURN:
                                            playSound(198, 50)
                                            coins-=int(1000*regenSpeed*1000*regenSpeed*1000*regenSpeed)
                                            regenSpeed+=0.001
                                        elif event.key==K_BACKSPACE:
                                            break
                   
for size in range(1,120):
    pygame.time.delay(2)
    drawText("GAME OVER!", size, (0, size*2, 0),650,350)
    pygame.display.update()
drawText("GAME OVER!", 120, (255,0,0),650,350)
pygame.display.update()
while True:
    for event in pygame.event.get():
        if (event.type==KEYUP and event.key==K_ESCAPE) or event.type==QUIT:
            done()
