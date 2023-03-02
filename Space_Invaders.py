
import pygame #bring in module to handle graphics, input, etc
import random
pygame.init() #set up pygame
pygame.display.set_caption("Space Invaders!") #set window title
screen = pygame.display.set_mode((800, 1000)) # creates game screen
clock = pygame.time.Clock() #SET UP CLOCK
gameover = False #variable to run game loop

#game variables
timer = 0
shoot = False
xpos = 400
ypos = 750
moveLeft = False
moveRight = False
numHits = 0
lives = 3



class Alien:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = True
        self.direction = 1
    def draw(self):
        if self.isAlive == True:
            pygame.draw.rect(screen, (250, 250, 250), (self.xpos, self.ypos, 40, 40))
        


    def collide(self, BulletX, BulletY):
        if self.isAlive:
            if BulletX > self.xpos and BulletX < self.xpos + 40 and BulletY < self.ypos + 40 and BulletY > self.ypos: #check if the bullet is bellow the top of the alien
                print("Hit!") #for testing
                self.isAlive = False #set the alien to dead
                return False #set the bullet to dead       
        return True
    def move(self, time):
        #resets direction every 8 moves
        if time % 600 == 0:
            self.ypos += 100
            self.direction *=-1
            return 0
        #move every tome the timer increases by 100
        if time % 150 == 0:
            self.xpos+=50*self.direction # move right

        return time

class Missile:
    def __init__(self):
        self.xpos = -10
        self.ypos = -10
        self.isAlive = False

    def move (self):
        if self.isAlive == True: #only shoot live bullets
            self.ypos+=5 #move up when shot
        if self.ypos > 800: #check if you've hit the top of the screen
            self.isAlive = False #set to dead
            self.xpos = -10 
            self.ypos = -10

    def draw(self):
        if self.isAlive == True:
            pygame.draw.rect(screen, (250, 250, 250), (self.xpos, self.ypos-17, 3, 20))

missile = []
for i in range (1):
    missile.append(Missile())



class Wall:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.numHits = 0
    def draw(self):
        if numHits == 0:
            pygame.draw.rect(screen, (255, 255, 0),(self.xpos, self.ypos, 30, 30))
        if numHits == 1:
            pygame.draw.rect(screen, (150, 150, 0), (self.xpos, self.ypos, 30, 30))
        if numHits == 2:
            pygame.draw.rect(screen, (50, 50, 0), (self.xpos, self.ypos, 30, 30))

    def collide(self, BulletX, BulletY):
        if self.numHits < 3:
            if BulletX > self.xpos and BulletX < self.xpos + 40 and BulletY < self.ypos + 40 and BulletY > self.ypos: #check if the bullet is bellow the top of the alien #for testing
                self.numHits += 1 #add hit to walls
                return numHits 
        
        return True 

walls = []
for k in range (4):
    for i in range (2):
        for j in range (3):
            walls.append(Wall(j*30+200*k+50, i*30+600))

class Bullet:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = False

    def move (self, xpos, ypos):
        if self.isAlive == True: #only shoot live bullets
            self.ypos-=5 #move up when shot
        if self.ypos < 0: #check if you've hit the top of the screen
            self.isAlive = False #set to dead
            self.xpos = xpos #reset to player position
            self.ypos = ypos

    def draw(self):
         pygame.draw.rect(screen, (250, 250, 250), (self.xpos, self.ypos-17, 3, 20))
#instantiate bullet object
bullet = Bullet(xpos+28, ypos) #create bullet and pass player position

armada = []#create empty list
for i in range (4): #handles rows
    for j in range (9): #handles columns
        armada.append(Alien(j*100+90, i*100+100)) # push alien objects into list

while not gameover: #game loop
#input section---------------------------
    clock.tick(60)# FPS
    timer += 1;
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True #quit game if x is pressedn in top corner

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveLeft = True
            elif event.key == pygame.K_RIGHT:
                moveRight = True
            elif event.key == pygame.K_SPACE:
                shoot = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moveLeft = False
            if event.key == pygame.K_RIGHT:
                moveRight = False
            if event.key == pygame.K_SPACE:
                shoot = False


#physics section--------------------------
    if moveLeft == True:
        vx =- 3
    elif moveRight == True:
        vx = 3
    else:
        vx = 0

    xpos += vx

    for i in range (len(armada)):
        timer = armada[i].move(timer)

    for i in range (len(missile)):
        missile[i].move()
        #print("moving missile!")

    if shoot == True:
        bullet.isAlive = True
        

    #check for wall/missile collision
    for i in range(len(walls)): #check each wall box
        for j in range(len(missile)): #against each missile
            if missile[j].isAlive == True: #check if missile is true
                if walls[i].collide(missile[j].xpos, missile[j].ypos) == False: #check wall collision for each combo
                    missile[j].isAlive = False #kill missile
                    print("killed missile!")
                    break #stop killing walls if you're dead!


    chance = random.randrange(100)
    if chance < 2:
        pick = random.randrange(len(armada))
        if armada[pick].isAlive == True:
            for i in range(len(missile)):
                if missile[i].isAlive == False:
                    missile[i].isAlive = True
                    missile[i].xpos = armada[pick].xpos+5
                    missile[i].ypos = armada[pick].ypos
                    break

    if bullet.isAlive == True:
        bullet.move(xpos+28, ypos)
        if bullet.isAlive == True:
            for i in range (len(armada)):
                bullet.isAlive = armada[i].collide(bullet.xpos, bullet.ypos)
                if bullet.isAlive == False:
                    break

        if bullet.isAlive == True:
            for i in range (len(walls)):
                bullet.isAlive = walls[i].collide(bullet.xpos, bullet.ypos)
                if bullet.isAlive == False:
                    break

    else:
        bullet.xpos = xpos + 28
        bullet.ypos = ypos


    for i in range (len(missile)):
        if missile[i].isAlive and missile[i].xpos > xpos and missile[i].xpos < xpos + 40 and missile[i].ypos < ypos + 40 and missile[i].ypos > ypos:
            print("Player Hit!")

    
#Render section------------------------------x
   
    screen.fill((0,0,0)) #wipe screen so it don't smear
   
    pygame.draw.rect(screen, (100, 0, 100), (xpos, 750, 60, 20)) # draw player
    pygame.draw.rect(screen, (100, 0, 100), (xpos+5, 745, 50, 20)) 
    pygame.draw.rect(screen, (100, 0, 100), (xpos+25, 736, 10, 20))
    pygame.draw.rect(screen, (100, 0, 100), (xpos+28, 732, 4, 20)) 

    bullet.draw()

    for i in range (len(armada)):
        armada[i].draw()

    for i in range (len(walls)):
        walls[i].draw()

    for i in range (len(missile)):
        missile[i].draw()

    


    
    pygame.display.flip()


    
#end game loop
    
pygame.quit()
  