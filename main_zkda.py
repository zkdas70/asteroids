import os
import sys
import pygame
from collections import Counter

pygame.init()
infos = pygame.display.Info()
screen_size = (infos.current_w, infos.current_h)
SIZE = WIDTH, HEIGHT = screen_size
screen = pygame.display.set_mode(SIZE)
FPS = 60
IS_DONT_TOUCH_IT = False
with open('data/seve', encoding='utf-8') as f_in:
    values = []
    for number, line in enumerate(f_in):
        values.append(str(line).replace('\n', ''))
    if values == ['True']:
        IS_DONT_TOUCH_IT = True
    f_in.close()


def komp():
    import random

    class Ball(pygame.sprite.Sprite):
        def __init__(self, radius, ):
            x = random.randint(50, height - 50)
            y = random.randint(50, width - 50)
            super().__init__(all_sprites)
            self.radius = radius
            self.image = pygame.Surface((2 * radius, 2 * radius),
                                        pygame.SRCALPHA, 32)
            pygame.draw.circle(self.image, pygame.Color((0, random.randint(100, 255), 0)),
                               (radius, radius), radius)
            self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
            self.vx = random.randint(-5, 5)
            self.vy = random.randrange(-5, 5)

        def update(self):
            self.rect = self.rect.move(self.vx, self.vy)
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.vy = -self.vy
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.vx = -self.vx

    class Border(pygame.sprite.Sprite):
        def __init__(self, x1, y1, x2, y2):
            super().__init__(all_sprites)
            if x1 == x2:  # вертикальная стенка
                self.add(vertical_borders)
                self.image = pygame.Surface([1, y2 - y1])
                self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
            else:  # горизонтальная стенка
                self.add(horizontal_borders)
                self.image = pygame.Surface([x2 - x1, 1])
                self.rect = pygame.Rect(x1, y1, x2 - x1, 1)

    FPS = 30
    size = width, height = WIDTH, HEIGHT
    pygame.init()
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    bak_color = pygame.Color('black')
    clock = pygame.time.Clock()
    running = True
    Border(5, 5, width - 5, 5)
    Border(5, height - 5, width - 5, height - 5)
    Border(5, 5, 5, height - 5)
    Border(width - 5, 5, width - 5, height - 5)
    for i in range(10):
        Ball(20)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                running = False
                break
        screen.fill(bak_color)
        all_sprites.draw(screen)
        hint('КАК ВЫЙТИ?', ['нажмите любую кнопку'], [(29, 153, 50), (26, 102, 38)])
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
    FPS = 60


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


def terminate_animation():
    FPS = 15
    size = WIDTH, HEIGHT
    pygame.init()
    screen = pygame.display.set_mode(size)
    BACK_COLOR = pygame.Color('black')

    class AnimatedSprite(pygame.sprite.Sprite):
        def __init__(self, x, y, sheet, columns, rows, paddings=(0, 0, 0, 0), count_frames=None):
            super().__init__(all_sprites)
            self.frames = []
            if count_frames is not None:
                self.count_frames = count_frames
            else:
                self.count_frames = columns * rows
            self.cut_sheet(sheet, columns, rows, paddings)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
            self.rect = self.rect.move(x, y)

        def cut_sheet(self, sheet, columns, rows, paddings):
            self.rect = pygame.Rect(0, 0, (sheet.get_width() - paddings[1] - paddings[3]) // columns,
                                    (sheet.get_height() - paddings[0] - paddings[2]) // rows)
            for j in range(rows):
                for i in range(columns):
                    frame_location = (paddings[3] + self.rect.w * i, paddings[0] + self.rect.h * j)
                    self.frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))
                    if len(self.frames) == self.count_frames:
                        break

        def update(self):
            self.cur_frame = (self.cur_frame + 1) % self.count_frames
            self.image = self.frames[self.cur_frame]

    class Boom(AnimatedSprite):
        img = load_image('boom.png')
        sheet = pygame.transform.scale(img, (WIDTH * 8, HEIGHT * 8))

        def __init__(self, x, y):
            super().__init__(x, y, self.__class__.sheet, 8, 8,
                             count_frames=41)

    if __name__ == '__main__':
        pygame.display.set_caption('Взрыв')
        clock = pygame.time.Clock()
        all_sprites = pygame.sprite.Group()
        Boom(20, 20)
        for _ in range(40):
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    break
            screen.fill(BACK_COLOR)
            all_sprites.update()
            all_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
    FPS = 60


def terminate():
    terminate_animation()
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "",
                  "",
                  "чтобы сбросить 'save' нажмите 'DELETE'"]

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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    IS_DONT_TOUCH_IT = False
                    with open('data/seve', 'w', encoding='utf-8') as f_out:
                        print(False, file=f_out)
                        f_out.close()
                else:
                    return  # начинаем игру
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def hint(title, text, colors=['Black', 'white']):
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

    text_drow(50, colors[0])
    text_drow(52, colors[1])


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
            elif level[y][x] == 'PS':
                Tile('P1', x, y)
                starship = pygame.sprite.Sprite()
                starship.image = load_image('Starship.png')
                starship.rect = starship.image.get_rect()
                all_sprites.add(starship)
                starship_group.add(starship)
                print(x, y)
                starship.rect.x = x * tile_width
                starship.rect.y = y * tile_height
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
        tiles = list((Counter(list(SPECIAL_TILES)) & Counter(tiles)))
        if tiles == ['pc']:
            hint('компьютер', ['для взаимодействия нажми "E"'])
        elif tiles == ['bt']:
            if IS_DONT_TOUCH_IT:
                hint('кнопка', ['для выхода из игры нажми нажми "E"'])
            else:
                hint('кнопка', ['для взаимодействия нажми "E"'])
        elif tiles == ['Ps']:
            hint('старшип', ['для взаимодействия нажми "E"'])
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if tiles == ['pc']:
                        komp()
                    elif tiles == ['bt']:
                        with open('data/seve', 'w', encoding='utf-8') as f_out:
                            print(True, file=f_out)
                            f_out.close()
                        terminate()
                    elif tiles == ['Ps']:
                        print('ec')
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.move(0, -1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.move(0, 1)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.move(-1, 0)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
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
    pygame.display.set_caption('Астероиды')
    clock = pygame.time.Clock()
    start_screen()
    WALL_TILES = ('W4',)
    FLOOR_TILES = ('PP', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'PX',)
    SPECIAL_TILES = ('pc', 'bt', 'Ps')
    PLAYER_TILE = 'P@'
    tile_images = {
        'W4': load_image('woll4.jpg'),
        'PP': load_image('pol.jpg'),
        'Ps': load_image('pol.jpg'),
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
    player_image = load_image('avatar.png')
    player = None
    camera = Camera()
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    starship_group = pygame.sprite.Group()
    player, level_x, level_y = generate_level(load_level('levelex.txt'))
    running = True
    while running:
        screen.fill((112, 146, 191))
        events = pygame.event.get()
        tiles_group.draw(screen)
        player_group.draw(screen)
        starship_group.draw(screen)
        player.update(events)
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        camera.update(player)  # изменяем ракурс камеры
        for sprite in all_sprites:  # обновляем положение всех спрайтов
            camera.apply(sprite)
        pygame.display.flip()
        clock.tick(FPS)
    terminate()
