####note: never do drawing in your main loop
import pygame
import math
pygame.init()

window = pygame.display.set_mode((500,480))
pygame.display.set_caption('Game')

###loading images
walkRight = [pygame.image.load('Game/R1.png'),pygame.image.load('Game/R2.png'),pygame.image.load('Game/R3.png'),pygame.image.load('Game/R4.png'),pygame.image.load('Game/R5.png'),pygame.image.load('Game/R6.png'),pygame.image.load('Game/R7.png'),pygame.image.load('Game/R8.png'),pygame.image.load('Game/R9.png')]
walkLeft = [pygame.image.load('Game/L1.png'),pygame.image.load('Game/L2.png'),pygame.image.load('Game/L3.png'),pygame.image.load('Game/L4.png'),pygame.image.load('Game/L5.png'),pygame.image.load('Game/L6.png'),pygame.image.load('Game/L7.png'),pygame.image.load('Game/L8.png'),pygame.image.load('Game/L9.png')]
backg = pygame.image.load('Game/bg.jpg')
standing = pygame.image.load('Game/standing.png')

bulletsound = pygame.mixer.Sound('Game/bulletshot.wav')
hitsound = pygame.mixer.Sound('Game/hit.wav')
jumpsound = pygame.mixer.Sound('Game/jump.wav')
music = pygame.mixer.Sound('Game/bgmusic.wav')
music.play(-1)

clock = pygame.time.Clock()

score = 0


class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkcount = 0
        self.isJump = False
        self.isstanding = True
        self.box = (self.x+20,self.y,28,50)
    
    def draw(self,window):
        if not self.isstanding:   
            if self.isJump:
                if self.left:
                    window.blit(walkLeft[0],(self.x,self.y))
                elif self.right:
                    window.blit(walkRight[0],(self.x,self.y))
            elif self.left:
                window.blit(walkLeft[self.walkcount//3],(self.x,self.y))
                self.walkcount += 1
            elif self.right:
                window.blit(walkRight[self.walkcount//3],(self.x,self.y))
                self.walkcount += 1
        else:
            if self.left:
                window.blit(walkLeft[0],(self.x,self.y))
            elif self.right:
                window.blit(walkRight[0],(self.x,self.y))
            else:
                window.blit(standing,(self.x,self.y))

        self.box = (self.x+18,self.y+12,29,50)
        #pygame.draw.rect(window,(255,255,255),self.box,2)

    def collision(self):
        ### if while jumping there is collison thne the player goes down the screen because the jumping hasnt stopeed when collison happened
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 410
        self.walkcount = 0
        font1 = pygame.font.SysFont('comicsans',100)
        text1 = font1.render('Reset!!! -5',1,(0,0,0))
        window.blit(text1,(250-(text1.get_width()/2),250-(text1.get_height()/2)))
        pygame.display.update()
        i = 0
        while i<300:
            pygame.time.delay(10)
            i+=1
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    i = 301
                    pygame.quit()
    
    def wining(self):
        #self.x = 60
        #self.y = 410
        #self.walkcount = 0
        font2 = pygame.font.SysFont('comicsans',40)
        text2 = font2.render('Congratulations',1,(255,255,255))
        window.fill((0,0,0))
        window.blit(text2,(250-(text2.get_width()/2),250-(text2.get_height()/2)))
        pygame.display.update()
        
class bullet_class(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * self.facing
    
    def draw(self,window):
        pygame.draw.circle(window,(0,0,0),(self.x,self.y),self.radius)
        pygame.draw.circle(window,self.color,(self.x,self.y),self.radius-1)
        

class enemy(object):
    walkRight = [pygame.image.load('Game/R1E.png'),pygame.image.load('Game/R2E.png'),pygame.image.load('Game/R3E.png'),pygame.image.load('Game/R4E.png'),pygame.image.load('Game/R5E.png'),pygame.image.load('Game/R6E.png'),pygame.image.load('Game/R7E.png'),pygame.image.load('Game/R8E.png'),pygame.image.load('Game/R9E.png'),pygame.image.load('Game/R10E.png'),pygame.image.load('Game/R11E.png')]
    walkLeft = [pygame.image.load('Game/L1E.png'),pygame.image.load('Game/L2E.png'),pygame.image.load('Game/L3E.png'),pygame.image.load('Game/L4E.png'),pygame.image.load('Game/L5E.png'),pygame.image.load('Game/L6E.png'),pygame.image.load('Game/L7E.png'),pygame.image.load('Game/L8E.png'),pygame.image.load('Game/L9E.png'),pygame.image.load('Game/L10E.png'),pygame.image.load('Game/L11E.png')]
    def __init__(self,x,y,width,height,end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        ### first element: start, sencond : end
        self.path = [self.x,self.end]
        self.walkcount = 0
        self.vel = 3
        self.box = (self.x+20,self.y,28,50)
        self.health = 10
        self.visible = True
    
    ###move increements or decreements x value hence before drawing calcuations are done 
    def draw(self,window):
        if self.visible:
            self.move()
            if self.walkcount + 1 >= 33:
                self.walkcount = 0

            if self.vel > 0:
                #pygame.draw.rect(window,(0,0,0),[(self.x,self.y),(self.x+64,self.y),(self.x,self.y-64),(self.x+64,self.y-64)],1)
                #pygame.display.update()
                window.blit(self.walkRight[self.walkcount//3], (self.x,self.y))
                self.walkcount = self.walkcount + 1
            else:
                #pygame.draw.rect(window,(0,0,0),(self.x,self.y,self.x+64,self.y+64),1)
                #pygame.display.update()
                #pygame.draw.rect(window,(0,0,0),(self.x,self.y,self.x+64,self.y+64))
                window.blit(self.walkLeft[self.walkcount//3], (self.x,self.y))
                self.walkcount = self.walkcount + 1
            self.box = (self.x+18,self.y+12,29,50)
            pygame.draw.rect(window,(0,0,0),(self.box[0],self.box[1]-20,50,10))
            pygame.draw.rect(window,(255,255,255),(self.box[0],self.box[1]-20,50-(5*(10-self.health)),10))
            #pygame.draw.rect(window,(255,255,255),self.box,2)
        
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x = self.x + self.vel
            else:
                ###reverses the enemy
                self.vel = self.vel * -1
                self.walkcount = 0
        
        else:
            if self.x - self.vel > self.path[0]:
                self.x = self.x + self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0
    
    def hit(self):
        if(self.health>0):
            self.health-=1
        else:
            self.visible = False
            window.fill((0,0,0))
        print('hit')
    
def drawGameWindow(walkcount):
    window.blit(backg,(0,0))
    ###will creata a surface and then blit it on window
    text = font.render('Score: '+str(score),1,(0,0,0))
    window.blit(text,(390,10))
    ###only this wont show rect
    
    #pygame.draw.rect(window,(0,255,0),(x,y,width,height))
    
    #print(math.floor(walkcount/3))
    ###adding this will show up
    man.draw(window)
    en.draw(window)
    for bullet in bullets:
        bullet.draw(window)
    pygame.display.update()



####main loop

if __name__=='__main__':
    
    font = pygame.font.SysFont('comicsans',30,True,True)
    man = player(60,410,64,64)
    en = enemy(100,410,64,64,450)
    ###only on a single press 3/4 bullets emanate that is the problem
    bulletlimit = 0
    run = True
    bullets = []
    
    #if(en.health<=0):
    #    box1 = (200,225,100,50)
    #    pygame.draw.rect(window,(255,255,255),box1)
    #    pygame.display.update()

    while run:
        ###for fps
        clock.tick(27)
        
        ####if enemy is down on health
        if en.health <= 0:
            del en
            man.wining()
            del man
            pygame.time.delay(3000)
            pygame.quit()
            
        #### collisoin of player with enemy
        if man.box[1] < en.box[1] + en.box[3] and man.box[1] + man.box[3] > en.box[1]:
            if man.box[0] + man.box[2] > en.box[0] + en.box[2] and man.box[0] < en.box[0] + en.box[2]:
                if(score>5):
                    score-=5
                else:
                    score = 0
                man.collision()

        if bulletlimit > 0:
            bulletlimit+=1
        if bulletlimit > 4:
            bulletlimit = 0
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
        for bullet in bullets:
            ####coliision:
            ##for y direction first: bullet.y - bullet.radius it represents bottom crease of bullet
            if bullet.y - bullet.radius < en.box[1] + en.box[3] and bullet.y + bullet.radius > en.box[1]:
                if bullet.x - bullet.radius < en.box[0] + en.box[2] and bullet.x + bullet.radius > en.box[0]:
                    hitsound.play()
                    en.hit()
                    score+=1
                    bullets.pop(bullets.index(bullet))
                    #pygame.draw.rect(window,(0,255,255),en.box)
    
            if bullet.x<500 and bullet.x>0:
                bullet.x = bullet.x + bullet.vel
            else:
                bullets.pop(bullets.index(bullet))
        #pygame.time.delay(100)

        if (man.walkcount + 1) >= 27:
            man.walkcount = 0
        man.walkcount = man.walkcount + 1
        drawGameWindow(man.walkcount)

        ##############IMPORTANT#####################
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and bulletlimit == 0:
            bulletsound.play()
            if man.left:
                facing = -1
            else:
                facing = 1
            if(len(bullets)<7):
                bullets.append(bullet_class(round(man.x+man.width//2),round(man.y+man.height//2), 4, (255,255,255),facing))
                #pygame.time.delay(10)
            bulletlimit = 1
            
        if keys[pygame.K_LEFT] and man.x>man.vel:
            man.x-=man.vel
            man.left = True
            man.right = False
            man.isstanding = False
        elif keys[pygame.K_RIGHT] and man.x+man.width+man.vel<500:
            man.x+=man.vel
            man.right = True
            man.left = False
            man.isstanding = False
        else:
            #man.left = False
            #man.right = False
            man.isstanding = True
            man.walkcount = 0

        ###jumping is only allowed if currently player is not in jump mode
        if not man.isJump:
           # if keys[pygame.K_UP] and y>vel:
           #     y-=vel
           # if keys[pygame.K_DOWN] and y+height+vel<500:
           #     y+=vel
            if keys[pygame.K_UP]:
                jumpsound.play()
                man.isJump = True
                man.left = False
                man.right = False
                man.walkcount = 0
        else:
            mul = 0.5
            #########if in jumping state
            if man.jumpCount >= -10:
                #### mul is used to make positive and negative increements while jumping
                if man.jumpCount < 0:
                    mul = -0.5
                man.y = man.y - (man.jumpCount**2 * mul)
                man.jumpCount = man.jumpCount - 1
            ######reset jumpcount and isjump as False
            else:
                man.jumpCount = 10
                man.isJump = False


        #window.fill((0,0,0))
    
    pygame.quit()
    quit()