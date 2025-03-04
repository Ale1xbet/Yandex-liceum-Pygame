import pygame
import os
import sys
import config
from random import randint

class Texture(pygame.sprite.Sprite):
    def __init__(self, image_name, x_pos, y_pos, *group):
        super().__init__(*group)
        fullname = os.path.join("Assets/" + image_name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()

        image = pygame.image.load(fullname)

        self.image = image
        self.rect = self.image.get_rect()

        self.rect.x = round((x_pos + 1 / 2) * config.SIZE - self.rect.width / 2)
        self.rect.y = round((y_pos + 1 / 2) * config.SIZE - self.rect.height / 2)


    def set_pos(self, x_pos, y_pos):
        self.rect.x = x_pos
        self.rect.y = y_pos


class Gamefield:
    def __init__(self, wid, hei, cll_sz, hero_pos):
        self.map = [[0 for _ in range(wid)] for __ in range(hei)]
        self.wid = wid
        self.hei = hei
        self.cell_size = cll_sz
        self.sprites = pygame.sprite.Group()
        self.hero_pos = hero_pos

        self.generate_walls()
        self.generate_ores()

    def generate_walls(self):
        cnt = 0
        while cnt != self.wid * self.hei // 5:
            coord = randint(0, self.wid * self.hei - 1)
            wl_x, wl_y = coord % self.wid, coord // self.wid
            if self.map[wl_y][wl_x] == 0 and [wl_y, wl_x] != [4, 4]:
                self.map[wl_y][wl_x] = 1

                cnt += 1


    def generate_ores(self):
        cnt = 0
        while cnt != self.wid * self.hei // 7:
            coord = randint(0, self.wid * self.hei - 1)
            ore_x, ore_y = coord % self.wid, coord // self.wid

            if self.map[ore_y][ore_x] == 0 and [ore_y, ore_x] != [4, 4]:
                self.map[ore_y][ore_x] = randint(2, 5) * 2 - 1

                cnt += 1


    def render_interface(self, stats, screen):
        iron_icon = Texture(config.TEXTURES[4], 0, 0, self.sprites)
        gold_icon = Texture(config.TEXTURES[6], 0, 0, self.sprites)
        diamond_icon = Texture(config.TEXTURES[8], 0, 0, self.sprites)
        emerald_icon = Texture(config.TEXTURES[10], 0, 0, self.sprites)

        iron_icon.set_pos(400, 5)
        gold_icon.set_pos(425, 5)
        diamond_icon.set_pos(450, 5)
        emerald_icon.set_pos(475, 5)

        font = pygame.font.Font(None, 16)
        text = font.render(str(config.STATS["iron"]), 1, "white")

        screen.blit(text, (410, 15))

        font = pygame.font.Font(None, 16)
        text = font.render(str(config.STATS["gold"]), 1, "white")

        screen.blit(text, (435, 15))

        font = pygame.font.Font(None, 16)
        text = font.render(str(config.STATS["diamond"]), 1, "white")

        screen.blit(text, (460, 15))

        font = pygame.font.Font(None, 16)
        text = font.render(str(config.STATS["emerald"]), 1, "white")

        screen.blit(text, (485, 15))



    def render_textures(self, screen):
        self.sprites.clear(screen, screen)
        for i in range(self.hei):
            for j in range(self.wid):
                object_id = self.map[i][j]
                new_sprite = Texture(config.TEXTURES[object_id], j, i, self.sprites)


    def render_hero(self):
        new_sprite = Texture(config.TEXTURES[2], self.hero_pos[0], self.hero_pos[1], self.sprites)


    def move_hero(self, direction):
        hr_x, hr_y = self.hero_pos

        if direction == "up":
            if hr_y != 0:
                if self.map[hr_y - 1][hr_x] != 1:
                    hr_y -= 1

        elif direction == "down":
            if hr_y != self.hei - 1:
                if self.map[hr_y + 1][hr_x] != 1:
                    hr_y += 1

        elif direction == "left":
            if hr_x != 0:
                if self.map[hr_y][hr_x - 1] != 1:
                    hr_x -= 1

        elif direction == "right":
            if hr_x != self.wid - 1:
                if self.map[hr_y][hr_x + 1] != 1:
                    hr_x += 1

        self.hero_pos = [hr_x, hr_y]


    def dig(self):
        hr_x, hr_y = self.hero_pos

        if self.map[hr_y][hr_x] not in [0, 1]:
            if self.map[hr_y][hr_x] == 3:
                self.map[hr_y][hr_x] = 0

                return "iron"

            elif self.map[hr_y][hr_x] == 5:
                self.map[hr_y][hr_x] = 0

                return "gold"

            elif self.map[hr_y][hr_x] == 7:
                self.map[hr_y][hr_x] = 0

                return "diamond"

            elif self.map[hr_y][hr_x] == 9:
                self.map[hr_y][hr_x] = 0

                return "emerald"

        return "nothing"

    def reset(self):
        self.map = [[0 for _ in range(self.wid)] for __ in range(self.hei)]
        self.hero_pos = [4, 4]
        self.generate_walls()
        self.generate_ores()
