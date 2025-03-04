import pygame
import gamefield
import config

clock = pygame.time.Clock()

if __name__ == "__main__":
    pygame.init()
    size = w, h = config.W, config.H

    screen = pygame.display.set_mode(size)

    all_sprites = pygame.sprite.Group()
    wallpaper = gamefield.Texture(config.TEXTURES[-1], 1, 2, all_sprites)

    all_sprites.draw(screen)
    pygame.display.flip()

    running = True
    waiting_for_click = True
    ores_collected = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and waiting_for_click:
                waiting_for_click = False

                game_field = gamefield.Gamefield(10, 10, config.SIZE, [4, 4])
                game_field.render_textures(screen)
                game_field.render_hero()
                game_field.render_interface(config.STATS, screen)
                game_field.sprites.draw(screen)
                game_field.render_interface(config.STATS, screen)
                pygame.display.flip()

            if not waiting_for_click:
                if ores_collected == 10 * 10 // 7:
                    ores_collected = 0

                    game_field.reset()
                    game_field.render_textures(screen)
                    game_field.render_hero()
                    game_field.render_interface(config.STATS, screen)
                    game_field.sprites.draw(screen)
                    game_field.render_interface(config.STATS, screen)
                    pygame.display.flip()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        game_field.move_hero("up")

                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        game_field.move_hero("down")

                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        game_field.move_hero("left")

                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        game_field.move_hero("right")

                    elif event.key == pygame.K_SPACE:
                        result = game_field.dig()

                        if result != "nothing":
                            config.STATS[result] += 1
                            ores_collected += 1

                    screen.fill((0, 0, 0))
                    game_field.render_textures(screen)
                    game_field.render_hero()
                    game_field.render_interface(config.STATS, screen)
                    game_field.sprites.draw(screen)
                    game_field.render_interface(config.STATS, screen)
                    pygame.display.flip()

                    print(1)

    pygame.quit()