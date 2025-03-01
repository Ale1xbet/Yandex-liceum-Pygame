import pygame.sprite
import config
import os
import sys


class BoardTexture(pygame.sprite.Sprite):
    def __init__(self, image_name, x_pos, y_pos, *group, screen_coords=False):
        super().__init__(*group)
        fullname = os.path.join("Assets/" + image_name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)

        self.image = image
        self.rect = self.image.get_rect()

        if screen_coords is False:
            self.rect.x = round((x_pos + 1/2) * config.SIZE - self.rect.width / 2)
            self.rect.y = round((y_pos + 1/2) * config.SIZE - self.rect.height / 2)
        else:
            self.rect.x = x_pos
            self.rect.y = y_pos