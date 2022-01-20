import os
import sys
import pygame
from collections import Counter

pygame.init()
SIZE = WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode(SIZE)
FPS = 50


def load_image(name, colorkey=None):
    fullname = os.path.join(r'data', 'sprites', name)
    if not os.path.isfile(fullname):  # если файл не существует, то выходим
        print(f"Файл с изображением '{fullname}' не найден")
        terminate()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def hint(title, text):
    intro_text = [title, ''] + text

    def text_drow(text_coord, color):
        font = pygame.font.Font(None, 30)
        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color(color))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    text_drow(50, 'Black')
    text_drow(52, 'white')


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip().split('|') for line in mapFile]
    return level_map


def generate_level(level):
    w = 0
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '':
                print(level[y][x])
                continue
            if level[y][x] == 'W4':
                Tile(level[y][x], x, y)
            elif level[y][x] in FLOOR_TILES:
                Tile(level[y][x], x, y)
            elif level[y][x] in SPECIAL_TILES:
                Tile(level[y][x], x, y)
            elif level[y][x] == PLAYER_TILE:
                Tile('PP', x, y)
                new_player = Player(level, x, y)
            else:
                Tile('ERROR', x, y)
    return new_player, len(level), len(level[y])


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, level, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.x = pos_x
        self.y = pos_y
        self.level = level
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15 + 10, tile_height * pos_y + 5 + 10)

    def move(self, dx, dy):
        x = (self.x + dx) % len(self.level[0])
        y = (self.y + dy) % len(self.level)
        if self.level[y][x] not in WALL_TILES:
            self.x = x
            self.y = y
            self.rect.move_ip(dx * tile_width, dy * tile_height)

    def update(self, events):
        tiles = [
            self.level[self.y - 1][self.x - 1], self.level[self.y - 1][self.x], self.level[self.y - 1][self.x + 1],
            self.level[self.y][self.x - 1], self.level[self.y][self.x], self.level[self.y][self.x + 1],
            self.level[self.y + 1][self.x - 1], self.level[self.y + 1][self.x], self.level[self.y + 1][self.x + 1],
        ]
        tiles = list((Counter(SPECIAL_TILES) & Counter(tiles)))
        if tiles == ['pc']:
            hint('компьютер', ['для взаимодействия нажми "E"'])
        elif tiles == ['bt']:
            hint('кнопка', ['для взаимодействия нажми "E"'])
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if tiles == ['pc']:
                        print('game of live')
                    elif tiles == ['bt']:
                        print('ec')
                if event.key == pygame.K_UP:
                    player.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    player.move(0, 1)
                elif event.key == pygame.K_LEFT:
                    player.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    player.move(1, 0)


class Camera:
    def __init__(self):  # зададим начальный сдвиг камеры
        self.target_fin_x = 0
        self.target_fin_y = 0
        self.dx = 0
        self.dy = 0

    def apply(self, obj):  # сдвинуть объект obj на смещение камеры
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):  # позиционировать камеру на объекте target
        self.target_fin_x = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.target_fin_y = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)
        self.dx = int(self.target_fin_x * 0.05)
        self.dy = int(self.target_fin_y * 0.05)


if __name__ == '__main__':
    BACK = pygame.Color('black ')
    pygame.display.set_caption('Перемещение героя. Новый уровень')
    clock = pygame.time.Clock()
    start_screen()
    WALL_TILES = ('W4',)
    FLOOR_TILES = ('PP', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'PX',)
    SPECIAL_TILES = ('pc', 'bt',)
    PLAYER_TILE = 'P@'
    tile_images = {
        'W4': load_image('woll4.jpg'),
        'PP': load_image('pol.jpg'),
        'P1': load_image('pol1.jpg'),
        'P2': load_image('pol2.jpg'),
        'P3': load_image('pol3.jpg'),
        'P4': load_image('pol4.jpg'),
        'P5': load_image('pol5.jpg'),
        'P6': load_image('pol6.jpg'),
        'P7': load_image('pol7.jpg'),
        'P8': load_image('pol8.jpg'),
        'P9': load_image('pol9.jpg'),
        'PX': load_image('polX.jpg'),
        'pc': load_image('pc.jpg'),
        'bt': load_image('btn.jpg'),
        'ERROR': load_image('ERROR.jpg'),
    }
    tile_width = tile_height = 60
    player_image = load_image('mario.png')
    player = None
    camera = Camera()
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    player, level_x, level_y = generate_level(load_level('levelex.txt'))
    running = True
    while running:
        screen.fill((112, 146, 191))
        events = pygame.event.get()
        player.update(events)
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    terminate()
