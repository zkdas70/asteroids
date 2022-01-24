import pygame
import sys
import os

pygame.init()
infos = pygame.display.Info()
screen_size = (infos.current_w, infos.current_h)
SIZE = WIDTH, HEIGHT = screen_size
screen = pygame.display.set_mode(SIZE)


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


def terminate():
    import animatioms_by_Зинич_Константин_Дмитриевич
    animatioms_by_Зинич_Константин_Дмитриевич.terminate_animation()
    pygame.quit()
    sys.exit()
