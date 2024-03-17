from pygame import *
from random import choice, randint
init()
font.init()
mixer.init()

screen_info = display.Info()
mixer.music.load('wind woosh loop.ogg')
fire_sound = mixer.Sound('fire.ogg')
mixer.music.set_volume(3)


mixer.music.play(-1)




WIDTH, HEIGHT = 1860, 1250
FPS = 360

font = font.SysFont('Arial', 35)
window = display.set_mode((WIDTH, HEIGHT), flags=FULLSCREEN)
display.set_caption('Shooter')
clock = time.Clock() #game timer

bg = image.load("back.png")
bg = transform.scale(bg, (WIDTH, HEIGHT)) #resize bg
bg_y1 = 0
bg_y2 = -HEIGHT


alien = image.load('alien.png')
asteroid = image.load('asteroid.png')
spaceship = image.load('spaceship.png')
bullet_image = image.load('lazer.png')




sprites = sprite.Group()
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, width=60, height=60, x=100, y=250):
        super().__init__()
        self.hp = 100
        self.image = transform.scale(sprite_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = mask.from_surface(self.image)
        sprites.add(self)
    def draw(self, window):
        window.blit(self.image, self.mask)
#code

class Player(GameSprite):
    
    def __init__(self, sprite_image, width=60, height=60, x=100, y=250):
        super().__init__(sprite_image,60,60, x, y)
        
        self.hp = 100
        self.damage = 20
        self.points = 0
        self.speed = 1

    def update(self):
        global hp_text
        self.old_pos = self.rect.x, self.rect.y
        keys = key.get_pressed()
        if keys[K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed

        collidelist = sprite.spritecollide(self, enemys, False, sprite.collide_mask)
        if len(collidelist) > 0:
            self.hp = 0
        
    def fire(self):
        Bullet(self.rect.x, self.rect.centery)
        fire_sound.play(0, 0, 1)

enemys = sprite.Group()
class Enemy(GameSprite):
    def __init__(self, width=100, height=70):
        x = randint(0, WIDTH)
        y = -150
        super().__init__(alien, width, height, x, y)
        self.speed = 1
        enemys.add(self)
    
    def update(self):
        global hp_text
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.kill()
        
        bullets_collide =sprite.groupcollide(bullets, enemys, True, True, sprite.collide_mask)
        collidelist = sprite.spritecollide(player, enemys, False, sprite.collide_mask)
        for enemy in collidelist:
            player.hp -= 10
            hp_text = font.render(f'HP:{player.hp}', True, (255, 255, 255))
            enemys.remove(self)
#        collidelist = sprite.spritecollide(self, bullets, True, sprite.collide_mask)
#        if len(collidelist) > 0:
#            self.kill()
        

bullets = sprite.Group()
class Bullet(GameSprite):
    def __init__(self, playerx, playery):
        super().__init__(bullet_image,20, 40, playerx, playery)
        self.speed = 7
        bullets.add(self)

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

player = Player(spaceship, 60, 60, 0, 600)

Enemy()
min_interval = 1000
max_interval = 5000
last_spawn_time = time.get_ticks()
randinterval = randint(min_interval, max_interval)

hp_text = font.render(f'HP:{player.hp}', True, (255, 255, 255))
points_text = font.render(f'Points:{player.points}', True, (255, 255, 255))

play = True
while play:

#оброби подію «клік за кнопкою "Закрити вікно"»
    for e in event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                player.fire()
    keys = key.get_pressed()
    if keys[K_a] and player.rect.left > 0:
        player.rect.x -= 1
    if keys[K_d] and player.rect.right < WIDTH:
        player.rect.x += 1
    if keys[K_ESCAPE]:
        quit()
    
    

    window.blit(bg, (0,bg_y1))
    window.blit(bg, (0,bg_y2))
    bg_y1 += 1
    bg_y2 += 1
    if bg_y1 > HEIGHT:
        bg_y1 = -HEIGHT
    if bg_y2 > HEIGHT:
        bg_y2 = -HEIGHT
    sprites.draw(window)
    if play:
        now = time.get_ticks()
        if randinterval < now - last_spawn_time:
            Enemy()
            if max_interval > min_interval:
                max_interval -= 10
            else:
                max_interval == min_interval
            last_spawn_time = time.get_ticks()
            randinterval = randint(min_interval, max_interval)
        sprites.update()
    if player.hp <= 0:
        play = True

    window.blit(hp_text, (10, 10))
    window.blit(points_text, (10, 50))
    
    display.update()
    clock.tick(FPS)
    