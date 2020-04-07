import tetris
import pygame

BLOCK_SIZE = 30
MAP_HEIGHT = 20 * BLOCK_SIZE + 4
MAP_WIDTH_FOR2 = 21 * BLOCK_SIZE + (2 * 180)
MAP_SIZE_FOR2 = [MAP_WIDTH_FOR2, MAP_HEIGHT]


def GameLoop2():
    global score
    global exist
    global game_over

    game_display = pygame.display.set_mode(MAP_SIZE_FOR2)
    left_block_grid = []
    right_block_grid = []
    middle_block_grid = []
    for _ in range(20):
        left_block_grid.append([None for _ in range(10)])
    for _ in range(20):
        right_block_grid.append([None for _ in range(10)])
    for _ in range(20):
        middle_block_grid.append([None])

    tet = tetris.Tetromino()
    tet.generate()
    r_tet = copy_generated_tetromino(tet)
    tet2 = tetris.Tetromino()
    tet2.generate()
    exist = True
    count = 1
    game_over = False
    score = 0
    level = 1

    while True:
        if exist is False:
            tet = copy_generated_tetromino(tet2)
            r_tet = copy_generated_tetromino(tet2)
            tet2.generate()
            tet.is_it_game_over(left_block_grid)
            r_tet.is_it_game_over(right_block_grid)
        if game_over:
            game = False
            while not game:
                game_display.fill((0, 0, 0))
                game_display.blit(tetris.game_over1, (40, 100))
                position = pygame.mouse.get_pos()
                game_display.blit(tetris.play_again1, (87, 250))
                if 87 < position[0] < 197 and 250 < position[1] < 280:
                    game_display.blit(tetris.play_again2, (87, 250))
                game_display.blit(tetris.main_menu1, (283, 250))
                if 283 < position[0] < 393 and 250 < position[1] < 280:
                    game_display.blit(tetris.main_menu2, (283, 250))
                game_display.blit(tetris.quit1, (35, 540))
                if 35 < position[0] < 145 and 540 < position[1] < 570:
                    game_display.blit(tetris.quit2, (35, 540))

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        tetris.game_exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            tetris.game_exit()
                        if event.key == pygame.K_c:
                            game_over = False
                            game = True
                            GameLoop2()
                        if event.key == pygame.K_m:
                            game_over = False
                            tetris.game_intro2()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if 87 < position[0] < 197 and 250 < position[1] < 280:
                            game_over = False
                            GameLoop2()
                        if 283 < position[0] < 393 and 250 < position[1] < 280:
                            game_over = False
                            tetris.game_intro2()
                        if 35 < position[0] < 145 and 540 < position[1] < 570:
                            tetris.game_exit()

        if count % (tetris.falling_speed[tetris.difficulty + level - 1]) == 0:
            tet.move_down(left_block_grid)
            r_tet.move_down(right_block_grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tetris.game_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if r_tet.can_right_go_left(right_block_grid,, None is True:
                        r_tet.move_horizontal(-1)
                if event.key == pygame.K_RIGHT:
                    if r_tet.can_go_right(right_block_grid) is True:
                        r_tet.move_horizontal(1)
                if event.key == pygame.K_UP:
                    r_tet.rotate(right_block_grid)
                if event.key == pygame.K_DOWN:
                    r_tet.move_down(right_block_grid)
                if event.key == pygame.K_SPACE:
                    r_tet.drop(right_block_grid)
                    #
                    #
                    #
                elif event.key == pygame.K_p:
                    tetris.pause()
        for line in range(20):
            to_eliminate = True
            for column in range(10):
                if right_block_grid[line][column] is None:
                    to_eliminate = False
            if to_eliminate is True:
                right_block_grid.pop(line)
                right_block_grid.insert(0, [None for _ in range(10)])
                middle_block_grid.pop(line)
                middle_block_grid.insert([None])
                score += 5
                if score % 100 == 0:
                    level += 1

            to_eliminate = True
            for column in range(10):
                if left_block_grid[line][column] is None:
                    to_eliminate = False
            if to_eliminate is True:
                left_block_grid.pop(line)
                left_block_grid.insert(0, [None for _ in range(10)])
                middle_block_grid.pop(line)
                middle_block_grid.insert([None])
                score += 5
                if score % 100 == 0:
                    level += 1

        game_display.fill((0, 0, 0))
        pygame.draw.rect(game_display, (255, 255, 255), [180, 2, 21 * BLOCK_SIZE, 20 * BLOCK_SIZE])
        # teraz rysujemy block grid
        for line in range(20):
            column = 0
            for color in right_block_grid[line]:  # iteruj po polach w linii block grida
                if color is not None:  # jeżeli jest tam zapisany jakiś kolor
                    pygame.draw.rect(game_display, (0, 0, 0),
                                     [180 + 11 * BLOCK_SIZE + column * BLOCK_SIZE, line * BLOCK_SIZE + 2, BLOCK_SIZE,
                                      BLOCK_SIZE])  # narysuj czarny kwadrat
                    pygame.draw.rect(game_display, color, [180 + 11 * BLOCK_SIZE + column * BLOCK_SIZE + 2, line * BLOCK_SIZE + 4, BLOCK_SIZE - 4,
                                                       BLOCK_SIZE - 4])  # w środku narysuj kwadrat o zadanym kolorze
                column += 1

        # teraz rysujemy spadający klocek
        for square in r_tet.squares:  # dla każdego kwadraciku
            # narysuj czarny kwadrat
            pygame.draw.rect(game_display, (0, 0, 0), [180 + 11 * BLOCK_SIZE + r_tet.pos[0] * BLOCK_SIZE + square[0] * BLOCK_SIZE,
                                                      r_tet.pos[1] * BLOCK_SIZE + 2 + square[1] * BLOCK_SIZE, BLOCK_SIZE,
                                                      BLOCK_SIZE])
            # w środku narysuj kwadrat o kolorze klocka
            pygame.draw.rect(game_display, tet.color, [180 + 11 * BLOCK_SIZE + r_tet.pos[0] * BLOCK_SIZE + 2 + square[0] * BLOCK_SIZE,
                                                       r_tet.pos[1] * BLOCK_SIZE + 4 + square[1] * BLOCK_SIZE,
                                                      BLOCK_SIZE - 4, BLOCK_SIZE - 4])

        my_font = pygame.font.SysFont("monospace", 20)
        text = my_font.render("Score = " + str(score), True, (255, 255, 255))
        game_display.blit(text, [324, 250])
        text2 = my_font.render("Level " + str(level), True, (255, 255, 255))
        game_display.blit(text2, [324, 220])

        pygame.draw.rect(game_display, (255, 255, 255), [17, 10, 150, 180])
        for square in tet2.squares:
            pygame.draw.rect(game_display, (0, 0, 0), [tet2.pos[0] * BLOCK_SIZE + 2 + square[0] * BLOCK_SIZE - 43,
                                                      tet2.pos[1] * BLOCK_SIZE + 2 + square[1] * BLOCK_SIZE + 30,
                                                      BLOCK_SIZE, BLOCK_SIZE])

        pygame.display.update()
        tetris.CLOCK.tick(tetris.FPS)
        count += 1


def copy_generated_tetromino(tetromino):
    tet = tetris.Tetromino()
    tet.color = tetromino.color
    tet.pos = tetromino.pos
    tet.squares = tetromino.squares
    return tet

