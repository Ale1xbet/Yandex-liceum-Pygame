import pygame
from random import randint
import math as m
import textures
import config

size = w, h = 10 * config.SIZE, 10 * config.SIZE

class Board:
    def __init__(self, width, height, cll_sz, level="default"):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = cll_sz
        self.sprites = pygame.sprite.Group()

        if level == "default":
            i = 19
            while i != 0:
                pos = randint(0, 99)
                x, y = pos % self.width, pos // self.width

                if (x, y) != (4, 4):
                    if self.board[y][x] == 0:
                        self.board[y][x] = 1
                        i -= 1
        else:
            self.load_level(level)

        self.print_board()

    def print_board(self, *hero_coords):
        board_copy = self.board[::]
        if hero_coords:
            x, y = hero_coords
            board_copy[y][x] = "*"

        for row in board_copy:
            print(*row)


    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size


    def get_cell(self, pos):
        cell_x = m.ceil((pos[0] - self.left) / self.cell_size)
        cell_y = m.ceil((pos[1] - self.top) / self.cell_size)

        if self.width >= cell_x >= 1 and self.height >= cell_y >= 1:
            return cell_x, cell_y
        else:
            return None


    def render(self):
        for i in range(self.height):
            for j in range(self.width):
                object_id = self.board[i][j]
                new_sprite = textures.BoardTexture(config.TEXTURES[object_id], j, i, self.sprites)

    def render_ores(self, screen):
        x, y = config.HERO_COORDS
        ore_sprites = pygame.sprite.Group()
        for ore_coords in config.ORES_COORDS["iron"]:
            o_x, o_y = ore_coords
            ch_x, ch_y = config.ABSOLUTE_HERO_COORDS
            if abs(o_x - ch_x) <= 5 and abs(o_y - ch_y) <= 5:
                related_coords = x + (o_x - ch_x), y + (o_y - ch_y)
                rel_x, rel_y = related_coords
                if self.board[rel_y][rel_x] == 0:
                    textures.BoardTexture(config.TEXTURES[3], 4 + o_x - ch_x, 4 - o_y + ch_y, ore_sprites)

        ore_sprites.draw(screen)
        


    def move_hero(self, direction):
        x, y = config.HERO_COORDS
        abs_x, abs_y = config.ABSOLUTE_HERO_COORDS
        mc = config.MOVE_COUNTER
        if direction == "up":
            if y != 0:
                if self.board[y - 1][x] == 0:
                    config.HERO_SPRITE.rect.y -= config.SIZE
                    y -= 1
                    abs_y += 1
                    mc += 1

        elif direction == "down":
            if y != self.height - 1:
                if self.board[y + 1][x] == 0:
                    config.HERO_SPRITE.rect.y += config.SIZE
                    y += 1
                    abs_y -= 1
                    mc += 1

        elif direction == "left":
            if x != 0:
                if self.board[y][x - 1] == 0:
                    config.HERO_SPRITE.rect.x -= config.SIZE
                    x -= 1
                    abs_x -= 1
                    mc += 1

        elif direction == "right":
            if x != self.width - 1:
                if self.board[y][x + 1] == 0:
                    config.HERO_SPRITE.rect.x += config.SIZE
                    x += 1
                    abs_x += 1
                    mac += 1

        config.ABSOLUTE_HERO_COORDS = [abs_x, abs_y]
        config.MOVE_COUNTER = mc
        config.HERO_COORDS= [x, y]
    

    def move_textures(self, direction):
        x, y = config.HERO_COORDS
        mc = config.MOVE_COUNTER
        abs_x, abs_y = config.ABSOLUTE_HERO_COORDS
        #self.print_board(x, y)

        if direction == "up":
            if y != 0:
                if self.board[y - 1][x] == 0:
                    for sprite in self.sprites:
                        sprite.rect.y += config.SIZE
                        if sprite.rect.y >= h:
                            sprite.rect.y = 0
                    
                    y -= 1
                    abs_y += 1
                    mc += 1
            else:
                if self.board[self.height - 1][x] == 0:
                    for sprite in self.sprites:
                        sprite.rect.y += config.SIZE
                        if sprite.rect.y >= h:
                            sprite.rect.y = 0

                    y = self.height - 1
                    abs_y += 1
                    mc += 1

        elif direction == "down":
            if y != self.height - 1:
                if self.board[y + 1][x] == 0:
                    for sprite in self.sprites:
                        sprite.rect.y -= config.SIZE
                        if sprite.rect.y < 0:
                            sprite.rect.y = h - config.SIZE
                    y += 1
                    abs_y -= 1
                    mc += 1

            else:
                if self.board[0][x] == 0:
                    for sprite in self.sprites:
                        sprite.rect.y -= config.SIZE
                        if sprite.rect.y < 0:
                            sprite.rect.y = h - config.SIZE
                    y = 0
                    abs_y -= 1
                    mc += 1

        elif direction == "left":
            if x != 0:
                if self.board[y][x - 1] == 0:
                    for sprite in self.sprites:
                        sprite.rect.x += config.SIZE
                        if sprite.rect.x >= w:
                            sprite.rect.x = 0
                    x -= 1
                    abs_x -= 1
                    mc += 1
            else:
                if self.board[y][self.width - 1] == 0:
                    for sprite in self.sprites:
                        sprite.rect.x += config.SIZE
                        if sprite.rect.x >= w:
                            sprite.rect.x = 0
                    x = self.width - 1
                    abs_x -= 1
                    mc += 1

        elif direction == "right":
            if x != self.width - 1:
                if self.board[y][x + 1] == 0:
                    for sprite in self.sprites:
                        sprite.rect.x -= config.SIZE
                        if sprite.rect.x < 0:
                            sprite.rect.x = w - config.SIZE
                    x += 1
                    abs_x += 1
                    mc += 1
            else:
                if self.board[y][0] == 0:
                    for sprite in self.sprites:
                        sprite.rect.x -= config.SIZE
                        if sprite.rect.x < 0:
                            sprite.rect.x = w - config.SIZE
                    x = 0
                    abs_x += 1
                    mc += 1

        config.ABSOLUTE_HERO_COORDS = [abs_x, abs_y]
        config.MOVE_COUNTER = mc
        config.HERO_COORDS= [x, y]


    def load_level(self, level_file):
        table = []
        try:
            with open(f"Data/{level_file}", "r") as f:
                for i in range(10):
                    row = f.readline().rstrip()
                    table.append([int(x) for x in row])
        except FileNotFoundError:
            print("Уровень не найден, загружаем случайный уровень.")

        self.board = table