import pygame, sys
from pygame.locals import *
from random import randint

# Creates the screen to draw on
pygame.init()
window = pygame.display.set_mode((1300,700))#,pygame.FULLSCREEN)
pygame.display.set_caption("Game 1","Game 1")

# Allows a key that is held down to count as multiple presses
pygame.key.set_repeat(1,1)

#Define Methods
def windowFill(red,green,blue):
    window.fill((red,green,blue))
def drawText(text, size, color, centerX, centerY):
    font=pygame.font.Font("PressStart2P.ttf", size)
    renderedText=font.render(text,True,color)
    textpos=renderedText.get_rect()
    textpos.centerx=centerX
    textpos.centery=centerY
    window.blit(renderedText, textpos)



#Initialize everything
HP=100
coins=0
score=0
speed=1
regenSpeed=0.001
coinOnScreen=False
chestOnScreen=False
chest=pygame.image.load("chest.gif")
chestOpened=pygame.image.load("chestOpened.gif")
dude=pygame.image.load("dude.gif")
dudeDamaged = pygame.image.load("dudeDamaged.gif")
guyX=randint(0,1250)
guyY=randint(0,650)
red=0
green=0
blue=0
HPr=0
HPg=255
#pygame.mouse.set_visible(False)

#Enemy Stuff
enemy1OnScreen=False
enemy2OnScreen=False
enemy1HP=0
enemy2HP=0
enemy1=pygame.image.load("enemy1.gif")
enemy1damaged=pygame.image.load("enemy1damaged.gif")
enemy2=pygame.image.load("enemy2.gif")
enemy2damaged=pygame.image.load("enemy2damaged.gif")
zombie=pygame.image.load("zombie.gif")
zombieDamaged=pygame.image.load("zombieDamaged.gif")
#[IMAGE, HP, SPEED, damage per loop (small, display of health is rounded)]
#enemy1=[10, 2, 0.05]
#enemy2=[20, 1, 10 (one time, also makes dude into Zombie)


# Event Loop
while HP>0:#Test this against while True for speed
    
    #Draw Background and words
    windowFill(red,green,blue)
    pygame.draw.rect(window, (50,50,50), (0,0,315,50),0)
    pygame.draw.line(window,(0,0,0) ,(125,0), (125,50), 5)
    drawText("+ SPEED: 1",12,(0, 0, 255),50,25)
    drawText("+ HP REGEN: 2",12,(255, 0, 255),220,25)
    drawText("COINS: "+str(coins), 26, (255,255,0),650,20)
    drawText("HP: "+str(int(HP//1)), 26, (HPr, HPg, 0),650,50)
    drawText("SCORE: "+str(score), 26, (255,255,0),1100,20)
    if enemy1OnScreen or enemy2OnScreen:
        drawText("TOTAL ENEMY HP: "+str(int(enemy1HP//1)+int(enemy2HP//1)), 26, (255,0,0),650,80)

    #Make Coin
    if not(coinOnScreen) and randint(1,500)==1:
        coinOnScreen=True
        coinX=randint(10,1290)
        coinY=randint(10,690)
    #Make Chest
    if not(chestOnScreen) and randint(1,10000)==1:
        chestOnScreen=True
        chestX=randint(16,1200)
        chestY=randint(1,639)
        
    #Draw Coin
    if coinOnScreen:
        pygame.draw.circle(window, (255,255,0),(coinX,coinY),8,0)
    #Draw Chest
    if chestOnScreen:
        window.blit(chest, (chestX, chestY))
        
    #Pick up Coin
    if coinOnScreen and coinX-guyX<60 and coinX-guyX>-5 and guyY-coinY>-60 and guyY-coinY<10:
        coinOnScreen=False
        coins+=1
        score+=10

    #Make Enemy1
    if not(enemy1OnScreen) and randint(1,1000)==1:
        enemy1OnScreen=True
        enemy1X=randint(0,1260)
        enemy1Y=randint(0,660)
        enemy1HP=10
    #Make Enemy2
    if not(enemy2OnScreen) and randint(1,1000)==1:
        enemy2OnScreen=True
        enemy2X=randint(0,1260)
        enemy2Y=randint(0,660)
        enemy2HP=20


    #Draw person on the screen
    window.blit(dude,(guyX,guyY))

    #Take damage from enemy1
    if enemy1OnScreen and enemy1X-guyX<48 and enemy1X-guyX>-32 and guyY-enemy1Y>-48 and guyY-enemy1Y<32:
        HP-=0.05
        window.blit(dudeDamaged,(guyX,guyY))
    #Take damage from enemy2
    if enemy2OnScreen and enemy2X-guyX<48 and enemy2X-guyX>-32 and guyY-enemy2Y>-48 and guyY-enemy2Y<32:
        HP/=2
        window.blit(dudeDamaged,(guyX,guyY))
        enemy2OnScreen=False
        enemy2HP=0
        
    #Change HP text color
    if HP>=50:
        HPr=0+5*(100-HP)
    else:
        HPr=255
    if HPr==255:
        HPg=255-5*(50-HP)

    #Move and draw enemy1
    if enemy1OnScreen:
        if enemy1X<guyX:
            enemy1X+=2
        if enemy1X>guyX:
            enemy1X-=2
        if enemy1Y<guyY:
            enemy1Y+=2
        if enemy1Y>guyY:
            enemy1Y-=2
        window.blit(enemy1, (enemy1X, enemy1Y))
    #Move and draw enemy2
    if enemy2OnScreen:
        if enemy2X<guyX:
            enemy2X+=1
        if enemy2X>guyX:
            enemy2X-=1
        if enemy2Y<guyY:
            enemy2Y+=1
        if enemy2Y>guyY:
            enemy2Y-=1
        window.blit(enemy2, (enemy2X, enemy2Y))

    #Damage enemy2 and check if dead
    if enemy1OnScreen and enemy2OnScreen and enemy1X-enemy2X<32 and enemy1X-enemy2X>-32 and enemy2Y-enemy1Y>-32 and enemy2Y-enemy1Y<32:
        enemy2HP-=0.25
        window.blit(enemy2damaged, (enemy2X,enemy2Y))
        if enemy2HP<=0:
            enemy2OnScreen=False
            coins+=25
            enemy2HP=0
            score+=500

    #Check if enemy1 is dead
    if enemy1OnScreen and enemy1HP<=0:
        enemy1OnScreen=False
        coins+=10
        enemy1HP=0
        score+=250

    #Regen HP
    if HP<100-regenSpeed:
        HP+=regenSpeed
    elif HP<100:
        HP=100

    #Open Chest
    if chestOnScreen and chestX-guyX<48 and chestX-guyX>-100 and guyY-chestY>-48 and guyY-chestY<60:
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
            pygame.quit()
            sys.exit()
        
        # Check if an arrow key is pressed and 
        # move guy in the correct direction
        elif event.type==KEYDOWN:

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
                
                    
            elif event.key==K_1:
                if speed>=5.999:
                    drawText("ALREADY AT MAXIMUM VELOCITY!", 24, (255, 0, 0),650,680)
                    pygame.display.update()

                elif coins<speed*speed*speed:
                    drawText("NOT ENOUGH COINS! Cost: "+str(speed*speed*speed), 24, (255, 127,0),650,680)
                    pygame.display.update()
                        
                else:
                    drawText("Confirm Purchase \"SPEED +1\" for "+str(speed*speed*speed)+" Coins? ENTER/BACKSPACE", 20, (0, 0, 255),650,680)
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
                                            coins-=int(1000*regenSpeed*1000*regenSpeed*1000*regenSpeed)
                                            regenSpeed+=0.001
                                        elif event.key==K_BACKSPACE:
                                            break

        elif event.type==KEYUP:
            if event.key==K_SPACE:
                if enemy1OnScreen and enemy1X-guyX<48 and enemy1X-guyX>-32 and guyY-enemy1Y>-48 and guyY-enemy1Y<32:#Damaging enemy1
                    enemy1HP-=1
                    window.blit(enemy1damaged, (enemy1X,enemy1Y))
                    pygame.display.update()
                    pygame.time.delay(100)

        if HP<=0:
            for size in range(1,120):
                drawText("GAME OVER!", size, (randint(0,255), randint(0,255), randint(0,255)),650,350)
                pygame.display.update()
            drawText("GAME OVER!", 120, (255,0,0),650,350)
            pygame.display.update()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()
