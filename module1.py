import pygame
import random

#écran
LARGEUR = 1920
HAUTEUR = 1080
FPS = 60

#Couleur
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)
JAUNE = (255, 255, 0)


#déplacement(vitesse)
SPEED = 8


pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Halloween's Space Shooter")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

background = pygame.image.load('./img/thumbnail_starfield.png').convert()
background_rect = background.get_rect()
player_img = pygame.image.load('./img/playerShip1_bleu.png').convert()
pumpkin_img = pygame.image.load('./img/pumpkin.png').convert()
skeleton_img = pygame.image.load('./img/skeleton.png').convert()
bullet_img = pygame.image.load('./img/laserRed16.png').convert()
H_V_img = pygame.image.load('./img/H_V.png').convert()
H_V2_img = pygame.image.load('./img/H_V2.png').convert()
H_J_img = pygame.image.load('./img/H_J.png').convert()
H_R_img = pygame.image.load('./img/H_R.png').convert()
H_0_img = pygame.image.load('./img/H_0.png').convert()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (10, 50))
        self.image.set_colorkey(NOIR)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
           self.kill()

class Ennemy1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = skeleton_img
        self.image.set_colorkey(NOIR)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(LARGEUR - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, SPEED)
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HAUTEUR + 10:
            self.rect.x = random.randrange(LARGEUR - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, SPEED)

class Ennemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pumpkin_img
        self.image.set_colorkey(NOIR)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(LARGEUR - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, SPEED)
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HAUTEUR + 10:
            self.rect.x = random.randrange(LARGEUR - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, SPEED)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pv = 100
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(NOIR)
        self.rect = self.image.get_rect()
        self.rect.centerx = LARGEUR / 2
        self.rect.bottom = HAUTEUR - 10
        self.speedx = 0
        self.speedy = 0
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
          self.speedx = -SPEED
        if keystate[pygame.K_RIGHT]:
          self.speedx = SPEED
        if keystate[pygame.K_UP]:
          self.speedy = -SPEED
        if keystate[pygame.K_DOWN]:
          self.speedy = SPEED
        if self.rect.right > LARGEUR:
            self.rect.right = LARGEUR
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HAUTEUR:
            self.rect.bottom = HAUTEUR
        if self.rect.top < 0:
            self.rect.top = 0
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

player = Player()
all_sprites.add(player)
ennemies = pygame.sprite.Group()
ennemies1 = pygame.sprite.Group()
for i in range(8):

    m = Ennemy()
    all_sprites.add(m)
    ennemies.add(m)

    m1 = Ennemy1()
    all_sprites.add(m1)
    ennemies1.add(m1)

bullets = pygame.sprite.Group()

class health_bars(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.health = 100
        self.image = H_V_img
        self.image.set_colorkey(BLANC)
        self.rect = self.image.get_rect()
    def perdvie(self, nb):
        self.health -= nb
    def update(self):
        if self.health < 75:
            self.image = H_V2_img
            self.image.set_colorkey(BLANC)
        elif self.health < 50:
            self.image = H_J_img
            self.image.set_colorkey(BLANC)
        else:
            self.image = H_R_img
            self.image.set_colorkey(BLANC)
     #   if self.health == 0:
      #      pygame.quit()

h = health_bars()
all_sprites.add(h)

   # pygame.draw.rect(health_bars(680, 25, player_health, 25))
#GameLoop
run = 1
while run == 1:
    clock.tick(FPS)
    all_sprites.update()
    hits = pygame.sprite.spritecollide(player, ennemies, False)
    if hits:
        hits_sound.play()
        h.perdvie(25)




    hits1 = pygame.sprite.spritecollide(player, ennemies1, False)
    if hits1:
        hits_sound.play()
        h.perdvie(25)


    hits = pygame.sprite.groupcollide(ennemies, bullets, True, True)
    for hit in hits:
        m = Ennemy()
        all_sprites.add(m)
        ennemies.add(m)
        kill_sound.play()

    hits1 = pygame.sprite.groupcollide(ennemies1, bullets, True, True)
    for hit in hits1:
        m1 = Ennemy1()
        all_sprites.add(m1)
        ennemies1.add(m1)
        kill1_sound.play()
    all_sprites.update()
    all_sprites.draw(window)
    pygame.display.flip()
    window.blit(background, background_rect)
   # health_bars(H_V_img)

    shoot_sound = pygame.mixer.Sound('./son/sfx_wpn_laser5.wav')
    shoot_sound.set_volume(0.10)
    kill_sound = pygame.mixer.Sound('./son/sfx_deathscream_human13.wav')
    kill_sound.set_volume(0.10)
    kill1_sound = pygame.mixer.Sound('./son/sfx_deathscream_human5.wav')
    kill1_sound.set_volume(0.10)
    hits_sound = pygame.mixer.Sound('./son/sfx_exp_short_hard1.wav')
    hits_sound.set_volume(0.10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

pygame.quit()

