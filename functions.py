import pygame
import gamefield
import config
import textures
from random import randint 

def gameCycle(*screen_params):
    pygame.init()
    size = w, h = 10 * config.SIZE, 10 * config.SIZE

    screen = pygame.display.set_mode(size)

    level_name = input()
    level_name = check_for_file(f"Assets/{level_name}")

    bckg_sprite = pygame.sprite.Group()
    hero_sprite = pygame.sprite.Group()
    statistics_sprites = pygame.sprite.Group()
    textures.BoardTexture(config.TEXTURES[4], w - 100, 15, statistics_sprites, screen_coords=True)
    textures.BoardTexture(config.TEXTURES[6], w - 75, 15, statistics_sprites, screen_coords=True)
    textures.BoardTexture(config.TEXTURES[8], w - 50, 15, statistics_sprites, screen_coords=True)
    textures.BoardTexture(config.TEXTURES[10], w - 25, 15, statistics_sprites, screen_coords=True)
    textures.BoardTexture(config.TEXTURES[11], 10, 15, statistics_sprites, screen_coords=True)
    background = textures.BoardTexture(config.TEXTURES[-1], 0, 0, bckg_sprite)
    background.rect.x = w / 2 - background.rect.width / 2
    background.rect.y = h / 2 - background.rect.height / 2

    bckg_sprite.draw(screen)
    pygame.display.flip()


    running = True
    game = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and game is False:
                game = True
                board = gamefield.Board(10, 10, config.SIZE, level_name)
                board.render()
                config.HERO_SPRITE = textures.BoardTexture(config.TEXTURES[2], config.HERO_COORDS[0], config.HERO_COORDS[1], hero_sprite)
                generate_ores()

                board.sprites.draw(screen)
                board.render_ores(screen)
                hero_sprite.draw(screen)
                statistics_sprites.draw(screen)
                pygame.display.flip()

            if game is True:
                if config.MOVE_COUNTER >= 100:
                    generate_ores()
                    print(config.ORES_COORDS)
                    config.MOVE_COUNTER = 0

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        board.move_hero("up")

                    elif event.key == pygame.K_s:
                        board.move_hero("down")

                    elif event.key == pygame.K_a:
                        board.move_hero("left")

                    elif event.key == pygame.K_d:
                        board.move_hero("right")
                    
                    elif event.key == pygame.K_DOWN:
                        board.move_textures("down")

                    elif event.key == pygame.K_UP:
                        board.move_textures("up")

                    elif event.key == pygame.K_RIGHT:
                        board.move_textures("right")

                    elif event.key == pygame.K_LEFT:
                        board.move_textures("left")

                    elif event.key == pygame.K_1:
                        board.load_level("level1.txt")
                        hero_sprite = pygame.sprite.Group()
                        board.render(screen)
                        config.HERO_COORDS = [4, 4]
                        HERO_SPRITE = gamefield.BoardTexture(config.TEXTURES[2], config.HERO_COORDS[0], config.HERO_COORDS[1], hero_sprite)

                    elif event.key == pygame.K_2:
                        board.load_level("level2.txt")
                        hero_sprite = pygame.sprite.Group()
                        board.render(screen)
                        config.HERO_COORDS = [4, 4]
                        HERO_SPRITE = gamefield.BoardTexture(config.TEXTURES[2], config.HERO_COORDS[0], config.HERO_COORDS[1], hero_sprite)

                    elif event.key == pygame.K_3:
                        board.load_level("level3.txt")
                        hero_sprite = pygame.sprite.Group()
                        board.render(screen)
                        config.HERO_COORDS = [4, 4]
                        HERO_SPRITE = gamefield.BoardTexture(config.TEXTURES[2], config.HERO_COORDS[0], config.HERO_COORDS[1], hero_sprite)

                    screen.fill((0, 0, 0))
                    board.sprites.draw(screen)
                    board.render_ores(screen)
                    hero_sprite.draw(screen)
                    statistics_sprites.draw(screen)
                    pygame.display.flip()

    pygame.quit()


def moveTable(table, direction):
    if direction == "up":
        if len(table) > 2:
            bottom_element = table[len(table) - 1]
            for i in range(len(table))[::-1]:
                table[i] = table[i - 1]

            table[0] = bottom_element


    elif direction == "down":
        if len(table) > 2:
            top_element = table[0]
            for i in range(len(table) - 1):
                table[i] = table[i + 1]

            table[len(table) - 1] = top_element

    elif direction == "left":
        if len(table[0]) > 2:
            for i in range(len(table)):
                right_element = table[i][len(table[i]) - 1]
                for j in range(len(table[i]))[::-1]:
                    table[i][j] = table[i][j - 1]

                table[i][0] = right_element

    elif direction == "right":
        if len(table[0]) > 2:
            for i in range(len(table)):
                left_element = table[i][0]
                for j in range(len(table[i]) - 1):
                    table[i][j] = table[i][j + 1]

                table[i][len(table[i]) - 1] = left_element

    return table


def check_for_file(f_name):
    try:
        open(f_name, "r")
        return f_name
    except FileNotFoundError:
        print("Файл не найден")
        f_name = "default"
        return f_name
        #sys.exit()
    except PermissionError:
        f_name = "default"
        return f_name
    

def generate_ores():
    g_x, g_y = config.ABSOLUTE_HERO_COORDS
    
    for x in range(g_x - 40, g_x + 40):
        for y in range(g_y - 40, g_y + 40):
            if x > g_x - 10 and x < g_x + 10 and y > g_y - 10 and y < g_y + 10:
                pass
            else:
                iron = randint(0, 1000) % 5 == 0
                gold = randint(0, 1000) % 10 == 5
                diamond = randint(0, 1000) % 25 == 0 and g_y <= -12
                emerald = randint(0, 1000) == 1 and g_x + g_y > 100

                if iron:
                    config.ORES_COORDS["iron"].append([x, y])

                elif gold:
                    config.ORES_COORDS["gold"].append([x, y])

                elif diamond:
                    config.ORES_COORDS["diamond"].append([x, y])

                elif emerald:
                    config.ORES_COORDS["emerald"].append([x, y])


                