import pygame
import random
from tkinter import Tk
from random import randrange as rnd


# Задаем размер экрана и некоторые параметры
tk = Tk()
SIZE = WIDTH, HEIGHT = tk.winfo_screenwidth(), tk.winfo_screenheight()
FPS = 60
STARS_COUNT = 300
METEORIT_COUNT = 10
star_list = []
pygame.display.set_caption('Beta test')
meteorit = pygame.image.load('meteorit.png')

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


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

    def update(self, *args):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.kill()
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
stars = pygame.sprite.Group()

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
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for bomb in mobs:
                bomb.update(event)

    # Обновление и рендеринг
    all_sprites.update()
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
