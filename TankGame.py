# Computer Science CPT - Dank Tanks
# Authors: Ethan Lee, Jamie Pinheiro
# Date: 2015/6/12
# Course: ICS3U1

import pygame
import random

#define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 100, 255]

#get the current highscore from file
def getHighScore():
    database = open("database_tank.txt", "r")
    highscore = int(database.readline())
    database.close()
    return highscore

#save highscore
def checkHighScore(score):
    database = open("database_tank.txt", "r")
    highscore = int(database.readline())
    database.close()
    #if highscore is less than current score
    if(highscore < score):
        database = open("database_tank.txt", "w")
        #save new score
        database.write(str(score))
        database.close

#find common factor
def GetCommonFactor(num):

    #make floats
    num[0] = float(num[0])
    num[1] = float(num[1])

    #lower to common 
    if(abs(num[0]) > abs(num[1])):
        num[1] = round(num[1] * 10/abs(num[0]))
        num[0] = round(num[0] * 10/abs(num[0]))
    elif(abs(num[0]) < abs(num[1])):
        num[0] = round(num[0] * 10/abs(num[1]))
        num[1] = round(num[1] * 10/abs(num[1]))

    return num

#rotate image
def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

#draw a ui bar
def drawUiBar(color, color2, value, position, size, screen):
    pygame.draw.rect(screen, color, [position[0], position[1], size[0] * value, size[1]])
    #check if value is not full
    if(value != 1):
        pygame.draw.rect(screen, color2, [position[0] + (size[0] * value), position[1], size[0] * (1 - value), size[1]])
            

#create grass2 object
class Grass2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Grass2, self).__init__()
        self.image = pygame.image.load("grass2.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
#create grass object
class Grass(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Grass, self).__init__()
        self.image = pygame.image.load("grass.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#create player tank
class Tank(pygame.sprite.Sprite):
    def __init__(self):
        super(Tank, self).__init__()
        self.image = pygame.image.load("player_tank.png").convert()
        self.image.set_colorkey(WHITE)
        self.image2 = rot_center(self.image,90)
        self.image3 = rot_center(self.image,180)
        self.image4 = rot_center(self.image,270)
        self.image5 = rot_center(self.image,45)
        self.image6 = rot_center(self.image,135)
        self.image7 = rot_center(self.image,225)
        self.image8 = rot_center(self.image,315)
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 440
        self.velocity = [0, 0]
        self.speed = 1
        self.rocketTimer = 0
        self.machineGunTimer = 0
        self.health = 1
        self.score = 0
    def move(self):
        #rotate tank based on direction it is traveling in
        if self.velocity[0] == 1 and self.velocity[1] == 1:
            self.image = self.image7
        if self.velocity[0] == -1 and self.velocity[1] == 1:
            self.image = self.image6
        if self.velocity[0] == -1 and self.velocity[1] == -1:
            self.image = self.image5
        if self.velocity[0] == 1 and self.velocity[1] == -1:
            self.image = self.image8
        if self.velocity[0] == 1 and self.velocity[1] == 0:
            self.image = self.image4
        if self.velocity[0] == -1 and self.velocity[1] == 0:
            self.image = self.image2
        if self.velocity[0] == 0 and self.velocity[1] == 1:
            self.image = self.image3
        if self.velocity[0] == 0 and self.velocity[1] == -1:
            self.image = rot_center(self.image3,180)

        self.rect.x += (self.velocity[0] * self.speed)
        self.rect.y += (self.velocity[1] * self.speed)
    def update(self):
        self.rocketTimer += (1.0/60.0)
        self.machineGunTimer += (1.0/60.0)
        #die if helath is less than 0
        if(self.health <= 0):
            pygame.sprite.Sprite.kill(self)
    def increaseScore(self,value):
        self.score += value

            

#create wall class
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Wall, self).__init__()
        self.image = pygame.image.load("wall.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 

#create rocket class
class Rocket(pygame.sprite.Sprite):
    def __init__(self, velocity, x, y):
        super(Rocket, self).__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = velocity
    def move(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
       
    def update(self):
        self.move()
        #if far off screen kill it
        if(self.rect.x < -100 or self.rect.x > 900):
            pygame.sprite.Sprite.kill(self)

#create bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, velocity, x, y):
        super(Bullet, self).__init__()
        self.image = pygame.Surface([4, 4])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = velocity
    def move(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
       
    def update(self):
        self.move()
        #if far off screen kill it
        if(self.rect.x < -100 or self.rect.x > 900):
            pygame.sprite.Sprite.kill(self)
            
#enemy tank
class EnemyTank(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(EnemyTank, self).__init__()
        self.image = pygame.image.load("enemy_tank.png").convert()
        self.image.set_colorkey(WHITE)
        self.image2 = rot_center(self.image,90)
        self.image3 = rot_center(self.image,180)
        self.image4 = rot_center(self.image,270)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 0.5
        self.velocity = [0,0]
        self.health = 1
    def move(self,playerPos):
        self.velocity = [playerPos[0] - self.rect.x + 5, playerPos[1] - self.rect.y + 5]
        self.velocity = GetCommonFactor(self.velocity)
        self.rect.x += self.velocity[0] * self.speed
        self.rect.y += self.velocity[1] * self.speed

        #rotate image based on rotation
        if self.velocity[0] > 0:
            self.image = self.image4
        if self.velocity[0] < 0:
            self.image = self.image2
        if self.velocity[1] > 0:
            self.image = self.image3
        if self.velocity[1] < 0:
            self.image = rot_center(self.image3,180)

    def update(self, playerPos):
        self.move(playerPos)
        #die if helath is less than 0
        if(self.health <= 0):
            pygame.sprite.Sprite.kill(self)
    def hit(self, value):
        self.health -= value
        
#main program
def main():
    pygame.init()
    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
    done = False
    clock = pygame.time.Clock()

    #background music
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.play(-1)
    
    terain_list = pygame.sprite.Group()
    tank_list = pygame.sprite.Group()
    wall_list = pygame.sprite.Group()
    bullet_list = pygame.sprite.Group()
    rocket_list = pygame.sprite.Group()
    enemy_tank_list = pygame.sprite.Group()
    
    screen_width = 800
    screen_height = 840
    screen = pygame.display.set_mode([screen_width, screen_height])
    pygame.display.set_caption("DANK TANKS")

    #font
    font = pygame.font.SysFont('Arial', 30, True, False)

    #spawn terrain
    for y in range(20):
        for x in range(20):
            #randomly decide if grass or grass2 on 20x20 grid
            if(random.randrange(0, 2) == 0):
                grass2 = Grass2(x * 40, y * 40 + 40)
                terain_list.add(grass2)
            else:
                grass = Grass(x * 40, y * 40 + 40)
                terain_list.add(grass)

    #spawn walls on 20 x 20 grid
    for y in range(20):
        for x in range(20):
            if(random.randrange(0, 10) == 0 or ((y == 0 or y == 19) or (x == 0 or x == 19))):
                if(x == 1):
                    if(y != 1 and y!= 18):
                        wall = Wall(x * 40, y * 40 + 40)
                        wall_list.add(wall)
                elif(x == 18):
                    if(y != 1 and y!= 18):
                        wall = Wall(x * 40, y * 40 + 40)
                        wall_list.add(wall)
                elif(x == 10):
                    if(y != 10):
                       wall = Wall(x * 40, y * 40 + 40)
                    wall_list.add(wall)
                else:
                    wall = Wall(x * 40, y * 40 + 40)
                    wall_list.add(wall)

    #create tank player
    tank = Tank()
    tank_list.add(tank)

    #create timers
    enemyTankTimer = 0
    enemySpawnTimer = -3
    hintTimer = 3
    time = 0

    #sounds
    bulletSound = pygame.mixer.Sound("bullet.ogg")
    rocketSound = pygame.mixer.Sound("rocket.ogg")

    #set spawntime
    spawnTime = 3

    while not done:

        #check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            #wasd movement
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w: 
                    tank.velocity = [tank.velocity[0], -1] 
                elif event.key == pygame.K_d:
                    tank.velocity = [1, tank.velocity[1]] 
                elif event.key == pygame.K_s:
                    tank.velocity = [tank.velocity[0], 1] 
                elif event.key == pygame.K_a:
                    tank.velocity = [-1, tank.velocity[1]]
                elif event.key == pygame.K_h:
                    hintTimer = 4
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w: 
                    tank.velocity = [tank.velocity[0], 0] 
                elif event.key == pygame.K_d:
                    tank.velocity = [0, tank.velocity[1]] 
                elif event.key == pygame.K_s:
                    tank.velocity = [tank.velocity[0], 0] 
                elif event.key == pygame.K_a:
                    tank.velocity = [0, tank.velocity[1]]
                elif event.key == pygame.K_h:
                    hintTimer = -1
                elif event.key == pygame.K_x:
                    if tank.health <= 0:
                        pygame.quit
                        main()
            #rocket
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    if(tank.rocketTimer > 3):
                        rocketSound.play()
                        mosPos = pygame.mouse.get_pos()
                        rocketVelocity = [mosPos[0] - tank.rect.x + 5, mosPos[1] - tank.rect.y + 5] 
                        if(rocketVelocity[0] == 0):
                            rocketVelocity[0] = 0.01
                        if(rocketVelocity[1] == 0):
                            rocketVelocity[1] = 0.01

                        rocketVelocity = GetCommonFactor(rocketVelocity)
                        
                        rocket = Rocket(rocketVelocity, tank.rect.x + 5, tank.rect.y + 5)    
                        rocket_list.add(rocket)
                        tank.rocketTimer = 0
        #machine gun
        if pygame.mouse.get_pressed()[0]:
            if(tank.machineGunTimer > 0.05):
                bulletSound.play()
                mosPos = pygame.mouse.get_pos()
                bulletVelocity = [mosPos[0] - tank.rect.x + 5, mosPos[1] - tank.rect.y + 5]
                #fix divied by zero error
                if(bulletVelocity[0] == 0):
                    bulletVelocity[0] = 0.01
                if(bulletVelocity[1] == 0):
                    bulletVelocity[1] = 0.01

                #lower to common factor
                bulletVelocity = GetCommonFactor(bulletVelocity)

                #create 2 bullets
                bullet1 = Bullet(bulletVelocity, tank.rect.x + 7, tank.rect.y + 7)
                bullet2 = Bullet(bulletVelocity, tank.rect.x + 3, tank.rect.y + 3)
                bullet_list.add(bullet1)
                bullet_list.add(bullet2)
                tank.machineGunTimer = 0

        #tank wall collisions
        wall_hit_list = pygame.sprite.spritecollide(tank, wall_list, False)
        
        for wall in wall_hit_list:
            if(tank.rect.y > (wall.rect.y - 5) and tank.rect.y < (wall.rect.y + 35)):
        
                if(tank.rect.x < wall.rect.x):
                    tank.rect.right = wall.rect.left
                elif(tank.rect.x > wall.rect.x):
                    tank.rect.left = wall.rect.right
            else:

                if(tank.rect.y < wall.rect.y):
                    tank.rect.bottom = wall.rect.top
                elif(tank.rect.y > wall.rect.y):
                    tank.rect.top = wall.rect.bottom

        #bullet collisions
        for wall in wall_list:
            #destroy bullets hitting walls
            bullet_hit_list = pygame.sprite.spritecollide(wall, bullet_list, True)
            bullet_hit_list = pygame.sprite.spritecollide(wall, rocket_list, True)
            #check enemy hitting wall
            enemy_tank_hit_list = pygame.sprite.spritecollide(wall, enemy_tank_list, False)

            #enemy and wall collisions
            for enemyTank in enemy_tank_hit_list:
                #collision comming from the side
                if(enemyTank.rect.y > (wall.rect.y - 5) and enemyTank.rect.y < (wall.rect.y + 35)):
                    if(enemyTank.rect.x < wall.rect.x):
                        enemyTank.rect.right = wall.rect.left
                    elif(enemyTank.rect.x > wall.rect.x):
                        enemyTank.rect.left = wall.rect.right
                #collision comming from the top
                else:
                    if(enemyTank.rect.y < wall.rect.y):
                        enemyTank.rect.bottom = wall.rect.top
                    elif(enemyTank.rect.y > wall.rect.y):
                        enemyTank.rect.top = wall.rect.bottom

                enemyTank.velocity = [0, 0]

        #enemy tank and bullet collisions
        for enemyTank in enemy_tank_list:
            bullet_hit_list = pygame.sprite.spritecollide(enemyTank, bullet_list, False)
            #damage enemy tank
            for bullet in bullet_hit_list:
                enemyTank.hit(0.04)
                pygame.sprite.Sprite.kill(bullet)
                tank.increaseScore(4)
                
            rocket_hit_list = pygame.sprite.spritecollide(enemyTank, rocket_list, False)
            #damage enemy tank 
            for rocket in rocket_hit_list:
                enemyTank.hit(1.0)
                pygame.sprite.Sprite.kill(rocket)
                tank.increaseScore(100)

        #tank and enemy tank collisions
        enemy_tank_hit_list = pygame.sprite.spritecollide(tank, enemy_tank_list, False)
        for enemyTank in enemy_tank_hit_list:
            pygame.sprite.Sprite.kill(enemyTank)
            tank.health -= 0.1

        #spawn enemies
        if enemySpawnTimer > spawnTime:
            #increase spawn rate
            if(spawnTime > 1):
                spawnTime -= 0.2
            rand = random.randrange(0, 3)
            rand2 = random.randrange(-5, 5)
            #spawn in one of the 4 corners
            if(rand == 0):
                enemytank = EnemyTank(60 + rand2, 100 + rand2)
            elif(rand == 1):
                enemytank = EnemyTank(740 + rand2, 100 + rand2)
            elif(rand == 2):
                enemytank = EnemyTank(740 + rand2, 780 + rand2)
            elif(rand == 3):
                enemytank = EnemyTank(60 + rand2, 780 + rand2)      
                
            enemy_tank_list.add(enemytank)
            enemySpawnTimer = 0

        #increment timers
        time += (1.0/60.0)
        enemyTankTimer += (1.0/60.0)
        enemySpawnTimer += (1.0/60.0)
        hintTimer -= (1.0/60.0)

        #moving and updates
        tank.move()
        tank.update()
        bullet_list.update()
        rocket_list.update()

        #move enemy tanks torwards player
        if enemyTankTimer > 0.25:
            enemy_tank_list.update([tank.rect.x,tank.rect.y])
            enemyTankTimer = 0

        #check high score
        checkHighScore(tank.score)

        #drawing sprites      
        screen.fill(WHITE)
        terain_list.draw(screen)
        wall_list.draw(screen)
        tank_list.draw(screen)
        bullet_list.draw(screen)
        rocket_list.draw(screen)
        
        #draw ui bars for tank  
        for enemyTank in enemy_tank_list:
            drawUiBar(GREEN, RED, enemyTank.health, [enemyTank.rect.x - 10, enemyTank.rect.y - 10], [50, 5], screen)        
        enemy_tank_list.draw(screen)
        if(tank.health > 0):
            drawUiBar(GREEN, RED, tank.health, [tank.rect.x - 20, tank.rect.y - 20], [70, 10], screen)
            if(tank.rocketTimer < 3):
                drawUiBar(BLUE, BLACK, tank.rocketTimer/3.0, [tank.rect.x - 20, tank.rect.y - 8], [70, 5], screen)
            else:
                drawUiBar(BLUE, BLACK, 1, [tank.rect.x - 20, tank.rect.y - 8], [70, 5], screen)


        #in game gui
        pygame.draw.rect(screen, BLUE, [0, 0, 800, 40])
        scoreText = font.render("SCORE: " + str(tank.score) + " High Score: " + str(getHighScore()), True, WHITE)
        timeTex = font.render(str(round(time * 100)/100.0) , True, WHITE)
        healthText = font.render(str(tank.health * 100) + "%", True, WHITE)
        screen.blit(scoreText,[250,2])
        screen.blit(timeTex,[700,2])
        screen.blit(healthText,[10,2])
        #show hint at start
        if(hintTimer > 0):
            pygame.draw.rect(screen, BLUE, [190, 280, 420, 250])
            hintText = font.render("WASD - Movement" , True, WHITE)
            hintText2 = font.render("Left Click - Machine Gun" , True, WHITE)
            hintText3 = font.render("Right Click - RPG" , True, WHITE)
            screen.blit(hintText,[280,300])
            screen.blit(hintText2,[250,380])
            screen.blit(hintText3,[280,460])

        #gameover screen
        if tank.health <= 0:
            pygame.draw.rect(screen, BLUE, [190, 280, 420, 200])
            endText = font.render("GAMEOVER" , True, WHITE)
            endText2 = font.render("Press x to play again." , True, WHITE)
            screen.blit(endText,[320,300])
            screen.blit(endText2,[280,380])

        #draw to screen
        pygame.display.flip()          
        clock.tick(60)
#run game
main()

#quit game
pygame.quit()
