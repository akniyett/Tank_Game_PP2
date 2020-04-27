import pygame
import random
from enum import Enum
import time

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((800, 600))

# def bg():
#     backgroundImage = pygame.image.load('wood5.jpg')
#     screen.blit(backgroundImage, (0, 0))


base = pygame.mixer.Sound('background1.wav')
base.play()

small = pygame.font.SysFont('comicsansms', 25)
med = pygame.font.SysFont('comicsansms', 35)
large = pygame.font.SysFont('comicsansms', 85)

class Direction(Enum):
    right = 1
    left = 2
    up = 3
    down = 4

    


class Tank:
    def __init__(self, x, y, speed, color, life, d_right = pygame.K_RIGHT, d_left = pygame.K_LEFT, d_up = pygame.K_UP, d_down = pygame.K_DOWN):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color 
        self.life = 3
        self.width = 40
        self.height = 40
        self.direction = Direction.right
        self.KEY = {d_right: Direction.right, d_left: Direction.left,
                    d_up: Direction.up, d_down: Direction.down}

    def draw(self):
        barrel = (self.x + self.width // 2, self.y + self.height // 2)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 2)
        pygame.draw.circle(screen, self.color, barrel, self.width // 2)

        if self.direction == Direction.right:
            pygame.draw.line(screen, self.color, barrel, (self.x + self.width + self.width // 2, self.y + self.height // 2), 4)

        if self.direction == Direction.left:
            pygame.draw.line(screen, self.color, barrel, (self.x - self.width + self.width // 2, self.y + self.width // 2), 4)
        
        if self.direction == Direction.up:
            pygame.draw.line(screen, self.color, barrel, (self.x + self.width // 2, self.y - self.width // 2), 4)

        if self.direction == Direction.down:
            pygame.draw.line(screen, self.color, barrel, (self.x + self.width // 2, self.y + self.height + self.width // 2), 4)

    def change_direction(self, direction):
        self.direction = direction

    def move(self):
        if self.direction == Direction.left:
            self.x -= self.speed
        if self.direction == Direction.right:
            self.x += self.speed
        if self.direction == Direction.up:
            self.y -= self.speed
        if self.direction == Direction.down:
            self.y += self.speed
        self.draw()
    
    
    def field(self):
        if self.x > 800:
            self.x = 0
        if self.x < 0:
           self.x = 800 
        if self.y < 0:
            self.y = 600
        if self.y > 600:
            self.y = 0
    
    def lifely(self):
        if self.life == 0:
            self.x = 1000
            self.y = 1000



tank1 = Tank(300, 300, 5, (69, 161, 69), 3)
tank2 = Tank(100, 100, 5, (50, 70, 194), 3, pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)
tanks = [tank1, tank2]

a = 0

class Bullet:
    def __init__(self, x, y, color, dx, dy):
        self.x = x
        self.y = y
        self.color = color
        self.dx = dx
        self.dy = dy
        self.drop = False
        
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 5)

    def shoot(self):
        a = self.dx
        a = self.dy
        self.x += self.dx
        self.y += self.dy
        self.draw()

    def launch(self, Tank):
        if Tank.direction == Direction.right:
            self.x = Tank.x + 60
            self.y = Tank.y + 20
            self.dx = a
            self.dy = 0 
        if Tank.direction == Direction.left:
            self.x = Tank.x - 60
            self.y = Tank.y + 20
            self.dx = -a
            self.dy = 0 
        if Tank.direction == Direction.up:
            self.x = Tank.x + 20
            self.y = Tank.y - 20
            self.dx = 0
            self.dy = -a
        if Tank.direction == Direction.down:
            self.x = Tank.x + 20
            self.y = Tank.y + 60
            self.dx = 0
            self.dy = a
        self.shoot()
    
    
    # def edge(self):
    #     if self.x > 800:
    #         self.x = 0
    #     if self.x < 0:
    #         self.x = 800
    #     if self.y > 600:
    #         self.y = 0
    #     if self.y < 0:
    #         self.y = 600

bullet1 = Bullet(900, 800, (69, 161, 69), 0, 0)
bullet2 = Bullet(900, 800, (50, 70, 194), 0, 0)
bullets = [bullet1, bullet2]

col = False

def open():
    welcome = large.render("Welcome to Tanks!", True, (255, 255, 102))
    screen.blit(welcome, (43, 50))

def intro():
    inf = med.render("You are gonna play with yourself!", True, (51, 255, 153))
    screen.blit(inf, (200, 200))

def collision(Bullet, Tank):
    col = False
    for bullet in bullets:
        if bullet.x in range(Tank.x, Tank.x + 40) and bullet.y in range(Tank.y, Tank.y + 40):
            bullet.x = 900
            bullet.y = 800
            col = True
    if col == True:
        Tank.life -= 1
           

def show():
    player_1 = small.render("player_1:", True, (69, 161, 69))
    screen.blit(player_1, (0, 5))
    life_count1 = small.render(str(tank1.life), True, (255, 255, 255))
    screen.blit(life_count1, (110, 5))
    player_2 = small.render("player_2:", True, (50, 70, 194))
    screen.blit(player_2, (670, 5))
    life_count2 = small.render(str(tank2.life), True, (255, 255, 255))
    screen.blit(life_count2, (780, 5))

def lost(Tank):
    if Tank.life == 0:
        Tank.x = 1000
        Tank.y = 1000





def text_objects(text, color, size = "small"):
    if size == "small":
        textSurface = small.render(text, True, color)
    if size == "medium":
        textSurface = med.render(text, True, color)
    if size == "large":
        textSurface = large.render(text, True, color)
    return textSurface, textSurface.get_rect()

def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size = "small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((buttonx + (buttonwidth//2)), buttony + (buttonheight // 2))
    screen.blit(textSurf, textRect)


muz = pygame.mixer.Sound('shooting.wav')

menu = True
running = True

start = pygame.mixer.Sound('start.wav')

while menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu = False
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu = False
                running = False
        
        

        screen.fill((153, 153, 255))
        # pygame.draw.rect(screen, (153, 255, 204), (150, 500, 100, 50))
        pygame.draw.rect(screen, (255, 153, 255), (150, 400, 100, 50))
        pygame.draw.rect(screen, (153, 204, 255), (350, 500, 100, 50))
        pygame.draw.rect(screen, (255, 102, 255), (350, 400, 100, 50))
        pygame.draw.rect(screen, (204, 0, 204), (550, 400, 100, 50))

        text_to_button('easy', (0, 0, 0),  150, 400, 100, 50)
        # text_to_button('tools', (0, 0, 0), 150, 500, 100, 50 )
        text_to_button('exit', (0, 0, 0),  350, 500, 100, 50)
        text_to_button('medium', (0, 0, 0), 350, 400, 100, 50)
        text_to_button('master', (0, 0, 0), 550, 400, 100, 50)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 150 < mouse[0] < 250 and 400 < mouse[1] < 450:  #easy
            pygame.draw.line(screen, (0, 0, 0), (170, 442), (230, 442))
            if click[0] == 1:
                running = True
                menu = False
                tank1.speed = 5
                tank2.speed = 5
                for bullet in bullets:
                    a = 10
                

        if 350 < mouse[0] < 450 and 400 < mouse[1] < 450:  #medium
            pygame.draw.line(screen, (0, 0, 0), (370, 442), (430, 442))
            if click[0] == 1:
                running = True
                menu = False
                tank1.speed = 10
                tank2.speed = 10
                for bullet in bullets:
                    a = 15


        if 550 < mouse[0] < 650 and 400 < mouse[1] < 450:  #master
            pygame.draw.line(screen, (0, 0, 0), (570, 442), (630, 442))
            if click[0] == 1:
                running = True
                menu = False
                tank1.speed = 15
                tank2.speed = 15
                for bullet in bullets:
                    a = 20


        if 350 < mouse[0] < 450 and 500 < mouse[1] < 550:   #exit
            pygame.draw.line(screen, (0, 0, 0), (370, 542), (430, 542))
            if click[0] == 1:
                running = False
                menu = False

        # if 150 < mouse[0] < 250 and 500 < mouse[1] < 550:   #tools
        #     pygame.draw.line(screen, (0, 0, 0), (170, 542), (230, 542))
        #     sound = True
        #     if click[0] == 1:
        #         pygame.mixer_music.pause()
                # sound = False
                # if click[0] == 1 and sound == False:
                #         pygame.mixer_music.unpause()
            #     # if event.type == pygame.MOUSEBUTTONUP:
            #         pygame.draw.rect(screen, (255, 102, 255), (350, 400, 100, 50))
            #         text_to_button("easy", (0, 0, 0), 350, 400, 100, 50)

        open()
        intro()
        pygame.display.flip()



FPS = 30
clock = pygame.time.Clock()

while running:
    
    mill = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                
            for i in tanks:
                if event.key in i.KEY.keys():
                    i.change_direction(i.KEY[event.key])



        
            if event.key == pygame.K_RETURN:
                muz.play()
                for i in bullets:
                    bullet1.launch(tank1)
            
            if event.key == pygame.K_SPACE:
                muz.play()
                for i in bullets:
                    bullet2.launch(tank2)

            pressed = pygame.key.get_pressed()
            
            if pressed[pygame.K_RETURN]:
                if len(bullets) >= 0:
                    bullet = Bullet(900, 800, (69, 161, 69), 0, 0)
                    bullets.append(bullet)
                    bullet.launch(tank1)
            if pressed[pygame.K_SPACE]:
                if len(bullets) >= 0:
                    bullet = Bullet(900, 800, (50, 70, 194), 0, 0)
                    bullets.append(bullet)
                    bullet.launch(tank2)
     
    screen.fill((0, 0, 0))
    # bg()
    if tank1.life == 0 or tank2.life == 0:
        base.stop()
        start.play()
        start.play()
        screen.fill((153, 153, 255))

        tank1.speed = 0
        tank2.speed = 0
        tank1.x = 200
        tank1.y = 250
        tank2.x = 600
        tank2.y = 250
        tank2.draw()
        tank1.draw()


        game_over = large.render("Game Over!", True, (255, 255, 102))
        screen.blit(game_over, (150, 100))
        if tank2.life == 0:
            winner_1 = med.render("Player_1  WON!", True, (51, 255, 153))
            screen.blit(winner_1, (250,350))
        if tank1.life == 0:
            winner_2 = med.render("Player_2 WON!", True, (51, 255, 153))
            screen.blit(winner_2, (250, 350))

        pygame.draw.rect(screen, (153, 204, 255), (350, 500, 100, 50))
        text_to_button('exit', (0, 0, 0),  350, 500, 100, 50)
        
        
        # pygame.draw.rect(screen, (153, 255, 204), (150, 500, 100, 50))
        # text_to_button('back', (0, 0, 0), 150, 500, 100, 50)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 350 < mouse[0] < 450 and 500 < mouse[1] < 550:   #exit
            pygame.draw.line(screen, (0, 0, 0), (370, 542), (430, 542))
            if click[0] == 1:
                running = False
                menu = False
        # if 150 < mouse[0] < 250 and 500 < mouse[1] < 550:   #tools
        #     pygame.draw.line(screen, (0, 0, 0), (170, 542), (230, 542))
        #     if click[0] == 1:
        #         menu = True
        #         running = False
                
        # running = False
        # menu = True

    for i in tanks:
        i.move()
        i.field()


    for i in bullets:
            i.shoot()
 


    
    collision(bullet1, tank2)
    collision(bullet2, tank1)
    
    lost(tank1)
    lost(tank2)
    show()
    pygame.display.flip()

pygame.quit()
