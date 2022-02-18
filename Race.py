import pygame
import random
from tkinter import Tk
from random import randrange as rnd


tk = Tk()
SIZE = WIDTH, HEIGHT = tk.winfo_screenwidth(), tk.winfo_screenheight()
Life = 3
FPS = 60
STARS_COUNT = 300
METEORIT_COUNT = 10
star_list = []
pygame.display.set_caption('Beta test')
meteorit = pygame.image.load('meteorit.png')
space = pygame.image.load('spaceship.png')
projectile = pygame.image.load('piu.png')
projectile = pygame.transform.rotate(projectile, 270)

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = space
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_d]:
            self.speedx = 8
        if keystate[pygame.K_s]:
            self.speedy = 8
        if keystate[pygame.K_w]:
            self.speedy = -8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH + 60:
            self.rect.right = WIDTH + 60
        if self.rect.left < -60:
            self.rect.left = -60
        if self.rect.top < HEIGHT - 400:
            self.rect.top = HEIGHT - 400
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Star(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((2, 2))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = rnd(WIDTH)
        self.rect.y = rnd(HEIGHT)

    def update(self):
        self.rect.y += 1
        if self.rect.y > HEIGHT:
            stt = Star_bot()
            stars.add(stt)
            all_sprites.add(stt)
            self.kill()


class Star_bot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((2, 2))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = rnd(WIDTH)
        self.rect.y = rnd(10)

    def update(self):
        self.rect.y += 1
        if self.rect.y > HEIGHT:
            stt = Star_bot()
            stars.add(stt)
            all_sprites.add(stt)
            self.kill()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = meteorit
        self.rect = self.image.get_rect()
        self.rect.x = rnd(WIDTH)
        self.rect.y = rnd(-100, -40)
        self.speedy = rnd(1, 3)
        self.speedx = rnd(-2, 2)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = projectile
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()


life = pygame.image.load('life.png')
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
stars = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for _ in range(STARS_COUNT):
    st = Star()
    stars.add(st)
    all_sprites.add(st)

for _ in range(METEORIT_COUNT):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            if event.key == pygame.K_ESCAPE:
                running = False

    # Обновление
    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    # Проверка, не ударил ли моб игрока и работа жизней
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_mask)
    if hits:
        Life -= 1

    if Life == 0:
        running = False

    # Рендеринг
    screen.fill(BLACK)
    all_sprites.draw(screen)
    for n in range(Life):
        screen.blit(life, (10 + n * 45, 800))
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
