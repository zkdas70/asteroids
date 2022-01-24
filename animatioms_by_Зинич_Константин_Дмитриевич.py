import pygame
from main_zkda_by_Зинич_Константин_Дмитриевич import load_image, WIDTH, HEIGHT


class amimatioms():
    def __init__(self):
        pass

    def terminate_animation(*self):
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
