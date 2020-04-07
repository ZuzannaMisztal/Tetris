import pygame
import random
import re
import copy

pygame.init()

BLOCK_SIZE = 30
BLOCK_SIZE2 = 20
MAP_HEIGHT = 20 * BLOCK_SIZE + 4
MAP_WIDTH = 10 * BLOCK_SIZE + 180
MAP_SIZE = [MAP_WIDTH, MAP_HEIGHT]
MAP_WIDTH_FOR2 = 21 * BLOCK_SIZE + (2 * 180)
MAP_SIZE_FOR2 = [MAP_WIDTH_FOR2, MAP_HEIGHT]
CLOCK = pygame.time.Clock()
FPS = 60
tetrisImg = pygame.image.load('tetris.png')
playImg = pygame.image.load('play.png')
play2Img = pygame.image.load('play2.png')
options1 = pygame.image.load('options.png')
options2 = pygame.image.load('options2.png')
options3 = pygame.image.load('options3.png')
highscore1 = pygame.image.load('highscore.png')
highscore2 = pygame.image.load('highscore2.png')
highscore3 = pygame.image.load('highscore3.png')
back = pygame.image.load('back.png')
back2 = pygame.image.load('back2.png')
tic = pygame.image.load('tic.png')
tic2 = pygame.image.load('tic2.png')
quit1 = pygame.image.load('quit.png')
quit2 = pygame.image.load('quit2.png')
play_again1 = pygame.image.load('play_again1.png')
play_again2 = pygame.image.load('play_again2.png')
continue1 = pygame.image.load('continue1.png')
continue2 = pygame.image.load('continue2.png')
main_menu1 = pygame.image.load('main_menu1.png')
main_menu2 = pygame.image.load('main_menu2.png')
game_over1 = pygame.image.load('game_over1.png')
pause1 = pygame.image.load('paused1.png')
easy1 = pygame.image.load('easy1.png')
easy2 = pygame.image.load('easy2.png')
medium1 = pygame.image.load('medium1.png')
medium2 = pygame.image.load('medium2.png')
hard1 = pygame.image.load('hard1.png')
hard2 = pygame.image.load('hard2.png')
my_font = pygame.font.SysFont("monospace", 20)
white = (255, 255, 255)

difficulty = 1
tetromines = [True, True, True, True, True, True, True, False, False, False, False]
animation_pos = [0, 0]
falling_speed = [40, 28, 24, 21, 18, 15, 13, 11, 10, 9, 9, 9, 9, 9]
rp_left = pygame.K_LEFT
lp_left = pygame.K_d
rp_right = pygame.K_RIGHT
lp_right = pygame.K_g
rp_up = pygame.K_UP
lp_up = pygame.K_r
rp_down = pygame.K_DOWN
lp_down = pygame.K_f
rp_drop = pygame.K_SPACE
lp_drop = pygame.K_z


def delete_lines(block_grid, middle_block_grid, right):
    global right_exist
    global left_exist
    global right_score
    global left_score
    global level
    for line in range(20):
        to_delete = True
        for column in range(10):
            if block_grid[line][column] is None:
                to_delete = False
                break
        if to_delete:
            block_grid.pop(line)
            block_grid.insert(0, [None for _ in range(10)])
            middle_block_grid.pop(line)
            middle_block_grid.insert(0, [None])
            if right:
                right_score += 5
            else:
                left_score += 5
            if (right_score + left_score) % 100 == 0 and level <= 9:
                level += 1


class Tetromino:
    def __init__(self):
        self.color = None
        self.pos = None
        self.squares = None

    def can_go_down(self, block_grid):
        global exist
        global game_over
        for square in self.squares:
            if self.pos[1] + square[1] == 19:  # jeżeli któryś z kwadratów jest na dole
                for square in self.squares:  # każdy kwadrat zapisz w block-gridzie
                    x = int(self.pos[0] + square[0])
                    y = int(self.pos[1] + square[1])
                    block_grid[y][x] = self.color
                    exist = False  # i przestań traktować jako klocek
                return False  # zwróć, że nie może pójść w dół
            x = int(self.pos[0] + square[0])
            y = int(self.pos[1] + square[1] + 1)
            if self.is_colliding(x, y, block_grid) is True:  # jeżeli gdyby był jeden niżej to by kolidował
                for square in self.squares:  # to samo co wyżej
                    x = int(self.pos[0] + square[0])
                    y = int(self.pos[1] + square[1])
                    block_grid[y][x] = self.color
                    exist = False
                return False
        return True  # jeżeli żaden z ifów nie jest spełniony, to znaczy, że może pójść w dół

    def can_go_left(self, block_grid):
        for square in self.squares:
            if self.pos[0] + square[0] == 0:  # jeżeli któryś z kwadratów jest już po lewej
                return False  # zwróć, że nie może pójść w lewo
            x = int(self.pos[0] + square[0] - 1)
            y = int(self.pos[1] + square[1])
            if self.is_colliding(x, y, block_grid) is True:  # jeżeli gdyby poszedł o jeden w lewo to by kolidował
                return False  # zwróć, że nie może iść w lewo
        return True  # jeżeli żaden z ifów nie jest spełniony, to znaczy, że może pójść w lewo

    def can_go_right(self, block_grid):
        for square in self.squares:
            if self.pos[0] + square[0] == 9:
                return False
            x = int(self.pos[0] + square[0] + 1)
            y = int(self.pos[1] + square[1])
            if self.is_colliding(x, y, block_grid) is True:
                return False
        return True

    def can_rotate(self, block_grid):
        if self.squares == [[0, 0], [1, 0], [0, 1], [1, 1]]:  # jeżeli to kwadrat, to nie obracaj
            return False
        for square in self.squares:
            x = int(self.pos[0] - square[1])
            y = int(self.pos[1] + square[0])
            if x < 0 or x > 9 or y < 0 or y > 19:  # jeżeli po obróceniu wychodziłoby za ścianki
                return False  # zwróc, że nie można obrócić
            if self.is_colliding(x, y, block_grid) is True:  # jeżeli któryś z kwadratów by kolidował
                return False  # zwróć, że nie można obrócić
        return True  # jeżeli żaden z ifów nie nie jest spełniony, to znaczy, że można obrócić

    def can_right_go_left(self, right_block_grid, middle_block_grid, l_tet):
        for square in self.squares:
            x = int(self.pos[0] + square[0] - 1)
            y = int(self.pos[1] + square[1])
            if x == -2:
                return False
            if x == -1:
                if self.is_colliding(0, y, middle_block_grid):
                    return False
                for l_square in l_tet.squares:
                    if l_tet.pos[0] + l_square[0] == 10 and l_tet.pos[1] + l_square[1] == y:
                        return False
            if self.is_colliding(x, y, right_block_grid) is True:
                return False
        return True

    def can_left_go_right(self, left_block_grid, middle_block_grid, r_tet):
        for square in self.squares:
            x = int(self.pos[0] + square[0] + 1)
            y = int(self.pos[1] + square[1])
            if x == 11:
                return False
            if x == 10:
                if self.is_colliding(0, y, middle_block_grid):
                    return False
                for r_square in r_tet.squares:
                    if r_tet.pos[0] + r_square[0] == -1 and r_tet.pos[1] + r_square[1] == y:
                        return False
            if self.is_colliding(x, y, left_block_grid) is True:
                return False
        return True

    def move_down(self, block_grid):
        if self.can_go_down(block_grid) is True:
            self.pos[1] += 1

    def move_horizontal(self, direction):
        self.pos[0] += direction

    def rotate(self, block_grid):
        if self.can_rotate(block_grid) is True:
            for square in self.squares:
                square[0], square[1] = -square[1], square[0]

    def drop(self, block_grid):
        while self.can_go_down(block_grid) is True:
            self.pos[1] += 1

    def drop2(self, block_grid, middle_block_grid, right):
        while self.can_go_down2(block_grid, middle_block_grid, right):
            self.pos[1] += 1

    def generate(self):
        global exist
        exist = True
        a = random.randrange(11)
        while not tetromines[a]:
            a = random.randrange(11)
        if a == 0:  # shapeO
            self.color = (255, 255, 0)  # yellow
            self.pos = [4, 0]
            self.squares = [[0, 0], [1, 0], [0, 1], [1, 1]]
        elif a == 1:  # shapeI
            self.color = (71, 0, 178)  # dark blue
            self.pos = [4, 2]
            self.squares = [[0, -2], [0, -1], [0, 0], [0, 1]]
        elif a == 2:  # shapeS
            self.color = (255, 0, 0)  # red
            self.pos = [4, 1]
            self.squares = [[-1, 0], [0, 0], [0, -1], [1, -1]]
        elif a == 3:  # shapeZ
            self.color = (0, 172, 23)  # dark green
            self.pos = [4, 1]
            self.squares = [[-1, -1], [0, -1], [0, 0], [1, 0]]
        elif a == 4:  # shapeL
            self.color = (255, 133, 0)  # orange
            self.pos = [4, 1]
            self.squares = [[0, -1], [0, 0], [0, 1], [1, 1]]
        elif a == 5:  # shapeJ
            self.color = (255, 133, 155)  # pink
            self.pos = [4, 1]
            self.squares = [[0, -1], [0, 0], [0, 1], [-1, 1]]
        elif a == 6:  # shapeT
            self.color = (0, 255, 255)  # light blue
            self.pos = [4, 1]
            self.squares = [[-1, 0], [0, 0], [1, 0], [0, -1]]
        elif a == 7:  # shapeL-3
            self.color = (114, 252, 64)
            self.pos = [4, 0]
            self.squares = [[0, 0], [1, 0], [1, 1]]
        elif a == 8:  # shapeI-3
            self.color = (186, 0, 155)
            self.pos = [4, 0]
            self.squares = [[0, 0], [1, 0], [2, 0]]
        elif a == 9:  # shape..
            self.color = (0, 94, 255)
            self.pos = [4, 0]
            self.squares = [[0, 0], [1, 0]]
        elif a == 10:  # shape.
            self.color = (128, 62, 0)
            self.pos = [4, 0]
            self.squares = [[0, 0]]

    def generate2(self):
        global left_exist
        global right_exist
        left_exist = True
        right_exist = True
        a = random.randrange(11)
        while tetromines[a] == False:
            a = random.randrange(11)
        if a == 0:  # shapeO
            self.color = (255, 255, 0)  # yellow
            self.pos = [4, 0]
            self.squares = [[0, 0], [1, 0], [0, 1], [1, 1]]
        elif a == 1:  # shapeI
            self.color = (71, 0, 178)  # dark blue
            self.pos = [4, 2]
            self.squares = [[0, -2], [0, -1], [0, 0], [0, 1]]
        elif a == 2:  # shapeS
            self.color = (255, 0, 0)  # red
            self.pos = [4, 1]
            self.squares = [[-1, 0], [0, 0], [0, -1], [1, -1]]
        elif a == 3:  # shapeZ
            self.color = (0, 172, 23)  # dark green
            self.pos = [4, 1]
            self.squares = [[-1, -1], [0, -1], [0, 0], [1, 0]]
        elif a == 4:  # shapeL
            self.color = (255, 133, 0)  # orange
            self.pos = [4, 1]
            self.squares = [[0, -1], [0, 0], [0, 1], [1, 1]]
        elif a == 5:  # shapeJ
            self.color = (255, 133, 155)  # pink
            self.pos = [4, 1]
            self.squares = [[0, -1], [0, 0], [0, 1], [-1, 1]]
        elif a == 6:  # shapeT
            self.color = (0, 255, 255)  # light blue
            self.pos = [4, 1]
            self.squares = [[-1, 0], [0, 0], [1, 0], [0, -1]]
        elif a == 7:  # shapeL-3
            self.color = (114, 252, 64)
            self.pos = [4, 0]
            self.squares = [[0, 0], [1, 0], [1, 1]]
        elif a == 8:  # shapeI-3
            self.color = (186, 0, 155)
            self.pos = [4, 0]
            self.squares = [[0, 0], [1, 0], [2, 0]]
        elif a == 9:  # shape..
            self.color = (0, 94, 255)
            self.pos = [4, 0]
            self.squares = [[0, 0], [1, 0]]
        elif a == 10:  # shape.
            self.color = (128, 62, 0)
            self.pos = [4, 0]
            self.squares = [[0, 0]]

    def is_it_game_over(self, block_grid):
        global game_over
        for square in self.squares:
            x = int(self.pos[0] + square[0])
            y = int(self.pos[1] + square[1])
            if self.is_colliding(x, y, block_grid) is True:
                game_over = True

    def move_down2(self, block_grid, middle_block_grid, right):
        if self.can_go_down2(block_grid, middle_block_grid, right):
            self.pos[1] += 1
        else:
            self.tetromino_down(block_grid, middle_block_grid, right)

    def can_go_down2(self, block_grid, middle_block_grid, right):
        for square in self.squares:
            x = self.pos[0] + square[0]
            y = self.pos[1] + square[1]
            if y == 19:
                return False
            if self.is_colliding(x, y + 1, block_grid) is True:
                return False
            if (right and x == -1) or (not right and x == 10):
                if self.is_colliding(0, y + 1, middle_block_grid):
                    return False
        return True

    def is_colliding(self, x, y, block_grid):
        if x <= -1 or x >= 10:
            return False
        if block_grid[y][x] is not None:
            return True
        else:
            return False

    def tetromino_down(self, block_grid, middle_block_grid, right):
        global left_exist
        global right_exist
        if right:
            right_exist = False
        else:
            left_exist = False
        for square in self.squares:
            x = self.pos[0] + square[0]
            y = self.pos[1] + square[1]
            if (right and x == -1) or (not right and x == 10):
                middle_block_grid[y][0] = self.color
            else:
                block_grid[y][x] = self.color
        delete_lines(block_grid, middle_block_grid, right)


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    position = pygame.mouse.get_pos()
                    if 38 < position[0] < 148 and 250 < position[1] < 280:
                        paused = False
                    if 185 < position[0] < 295 and 250 < position[1] < 280:
                        paused = False
                        GameLoop()
                    if 332 < position[0] < 442 and 250 < position[1] < 280:
                        paused = False
                        game_intro2()
                    if 35 < position[0] < 145 and 540 < position[1] < 570:
                        game_exit()

        gameDisplay.fill((0, 0, 0))
        position = pygame.mouse.get_pos()
        gameDisplay.blit(pause1, (100, 60))
        gameDisplay.blit(continue1, (38, 250))
        if 38 < position[0] < 148 and 250 < position[1] < 280:
            gameDisplay.blit(continue2, (38, 250))
        gameDisplay.blit(play_again1, (185, 250))
        if 185 < position[0] < 295 and 250 < position[1] < 280:
            gameDisplay.blit(play_again2, (185, 250))
        gameDisplay.blit(main_menu1, (332, 250))
        if 332 < position[0] < 442 and 250 < position[1] < 280:
            gameDisplay.blit(main_menu2, (332, 250))
        gameDisplay.blit(quit1, (35, 540))
        if 35 < position[0] < 145 and 540 < position[1] < 570:
            gameDisplay.blit(quit2, (35, 540))
        pygame.display.update()
        CLOCK.tick(FPS)


def game_intro2():
    intro = True
    sprite = pygame.image.load("Zuziamenu.png")
    im_x = 16
    cur_x = animation_pos[0]
    cur_y = animation_pos[1]

    slow = 0

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_exit()
                if event.key == pygame.K_c:
                    intro = False
                    GameLoop2()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    position = pygame.mouse.get_pos()
                    if 35 < position[0] < 145 and 80 < position[1] < 110:
                        intro = False
                        animation_pos[0] = 0
                        animation_pos[1] = 0
                        GameLoop()
                    if 35 < position[0] < 145 and 140 < position[1] < 170:
                        intro = False
                        animation_pos[0] = cur_x
                        animation_pos[1] = cur_y
                        options()
                    if 35 < position[0] < 145 and 200 < position[1] < 230:
                        intro = False
                        animation_pos[0] = 0
                        animation_pos[1] = 0
                        highscore()
                    if 35 < position[0] < 145 and 540 < position[1] < 570:
                        game_exit()

        gameDisplay.fill((0, 0, 0))
        slow += 1
        if slow % 8 == 0:
            if cur_x >= im_x - 1:
                if cur_y == 15 and cur_x == 15:
                    cur_y = cur_x = 0
                else:
                    cur_y += 1
                    cur_x = 0
            else:
                cur_x += 1
        gameDisplay.blit(sprite, (178, 2), [cur_x * 300, cur_y * 600, 300, 600])

        gameDisplay.blit(tetrisImg, (15, 10))
        position = pygame.mouse.get_pos()
        gameDisplay.blit(playImg, (35, 80))
        if 35 < position[0] < 145 and 80 < position[1] < 110:
            gameDisplay.blit(play2Img, (35, 80))
        gameDisplay.blit(options1, (35, 140))
        if 35 < position[0] < 145 and 140 < position[1] < 170:
            gameDisplay.blit(options2, (35, 140))
        gameDisplay.blit(highscore1, (35, 200))
        if 35 < position[0] < 145 and 200 < position[1] < 230:
            gameDisplay.blit(highscore2, (35, 200))
        gameDisplay.blit(quit1, (35, 540))
        if 35 < position[0] < 145 and 540 < position[1] < 570:
            gameDisplay.blit(quit2, (35, 540))
        pygame.display.update()
        CLOCK.tick(FPS)


def left_controls():
    global lp_left
    global lp_right
    global lp_up
    global lp_down
    global lp_drop

    left_controls = True
    title = my_font.render("Left player controls", True, white)
    left = my_font.render("Left", True, white)
    right = my_font.render("Right", True, white)
    down = my_font.render("Down", True, white)
    rotate = my_font.render("Rotate", True, white)
    drop = my_font.render("Drop", True, white)

    while left_controls:
        gameDisplay.fill((0, 0, 0))
        gameDisplay.blit(title, [120, 30])
        gameDisplay.blit(left, [100, 100])
        gameDisplay.blit(right, [100, 175])
        gameDisplay.blit(down, [100, 250])
        gameDisplay.blit(rotate, [100, 325])
        gameDisplay.blit(drop, [100, 400])
        chosen_left = my_font.render(pygame.key.name(lp_left), True, white)
        chosen_right = my_font.render(pygame.key.name(lp_right), True, white)
        chosen_down = my_font.render(pygame.key.name(lp_down), True, white)
        chosen_up = my_font.render(pygame.key.name(lp_up), True, white)
        chosen_drop =  my_font.render(pygame.key.name(lp_drop), True, white)
        gameDisplay.blit(chosen_left, [300, 100])
        gameDisplay.blit(chosen_right, [300, 175])
        gameDisplay.blit(chosen_down, [300, 250])
        gameDisplay.blit(chosen_up, [300, 325])
        gameDisplay.blit(chosen_drop, [300, 400])
        position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    if 35 < position[0] < 145 and 540 < position[1] < 570:
                        options()
                    if 300 < position[0] < 340 and 100 < position[1] < 140:
                        get_key = True
                        while get_key:
                            for event_1 in pygame.event.get():
                                if event_1.type == pygame.KEYDOWN:
                                    lp_left = event_1.key
                                    get_key = False
                    if 300 < position[0] < 340 and 175 < position[1] < 215:
                        get_key = True
                        while get_key:
                            for event_1 in pygame.event.get():
                                if event_1.type == pygame.KEYDOWN:
                                    lp_right = event_1.key
                                    get_key = False
                    if 300 < position[0] < 340 and 250 < position[1] < 290:
                        get_key = True
                        while get_key:
                            for event_1 in pygame.event.get():
                                if event_1.type == pygame.KEYDOWN:
                                    lp_down = event_1.key
                                    get_key = False
                    if 300 < position[0] < 340 and 315 < position[1] < 355:
                        get_key = True
                        while get_key:
                            for event_1 in pygame.event.get():
                                if event_1.type == pygame.KEYDOWN:
                                    lp_up = event_1.key
                                    get_key = False
                    if 300 < position[0] < 340 and 400 < position[1] < 440:
                        get_key = True
                        while get_key:
                            for event_1 in pygame.event.get():
                                if event_1.type == pygame.KEYDOWN:
                                    lp_drop= event_1.key
                                    get_key = False

        gameDisplay.blit(back, (35, 540))
        if 35 < position[0] < 145 and 540 < position[1] < 570:
            gameDisplay.blit(back2, (35, 540))
        pygame.display.update()
        CLOCK.tick(FPS)


def right_controls():
    global rp_left
    global rp_right
    global rp_up
    global rp_down
    global rp_drop

    right_controls = True
    white = (255, 255, 255)
    title = my_font.render("Right player controls", True, white)
    left = my_font.render("Left", True, white)
    right = my_font.render("Right", True, white)
    down = my_font.render("Down", True, white)
    rotate = my_font.render("Rotate", True, white)
    drop = my_font.render("Drop", True, white)

    while right_controls:
        gameDisplay.fill((0, 0, 0))
        gameDisplay.blit(title, [120, 30])
        gameDisplay.blit(left, [100, 100])
        gameDisplay.blit(right, [100, 175])
        gameDisplay.blit(down, [100, 250])
        gameDisplay.blit(rotate, [100, 325])
        gameDisplay.blit(drop, [100, 400])
        chosen_left = my_font.render(pygame.key.name(rp_left), True, white)
        chosen_right = my_font.render(pygame.key.name(rp_right), True, white)
        chosen_down = my_font.render(pygame.key.name(rp_down), True, white)
        chosen_up = my_font.render(pygame.key.name(rp_up), True, white)
        chosen_drop = my_font.render(pygame.key.name(rp_drop), True, white)
        gameDisplay.blit(chosen_left, [300, 100])
        gameDisplay.blit(chosen_right, [300, 175])
        gameDisplay.blit(chosen_down, [300, 250])
        gameDisplay.blit(chosen_up, [300, 325])
        gameDisplay.blit(chosen_drop, [300, 400])
        position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    if 35 < position[0] < 145 and 540 < position[1] < 570:
                        options()
                    if 300 < position[0] < 340 and 100 < position[1] < 140:
                        get_key = True
                        while get_key:
                            for event_1 in pygame.event.get():
                                if event_1.type == pygame.KEYDOWN:
                                    rp_left = event_1.key
                                    get_key = False
                    if 300 < position[0] < 340 and 175 < position[1] < 215:
                        get_key = True
                        while get_key:
                            for event_1 in pygame.event.get():
                                if event_1.type == pygame.KEYDOWN:
                                    rp_right = event_1.key
                                    get_key = False
                    if 300 < position[0] < 340 and 250 < position[1] < 290:
                        get_key = True
                        while get_key:
                            for event_1 in pygame.event.get():
                                if event_1.type == pygame.KEYDOWN:
                                    rp_down = event_1.key
                                    get_key = False
                    if 300 < position[0] < 340 and 315 < position[1] < 355:
                        get_key = True
                        while get_key:
                            for event_1 in pygame.event.get():
                                if event_1.type == pygame.KEYDOWN:
                                    rp_up = event_1.key
                                    get_key = False
                    if 300 < position[0] < 340 and 400 < position[1] < 440:
                        get_key = True
                        while get_key:
                            for event_1 in pygame.event.get():
                                if event_1.type == pygame.KEYDOWN:
                                    rp_drop = event_1.key
                                    get_key = False

        gameDisplay.blit(back, (35, 540))
        if 35 < position[0] < 145 and 540 < position[1] < 570:
            gameDisplay.blit(back2, (35, 540))
        pygame.display.update()
        CLOCK.tick(FPS)


def options():
    global difficulty
    gameDisplay.fill((0, 0, 0))
    gameDisplay.blit(options3, (160, 10))
    text = my_font.render("Left controls", True, (255, 255, 255))
    gameDisplay.blit(text, [38, 475])
    text = my_font.render("Right controls", True, (255, 255, 255))
    gameDisplay.blit(text, [270, 475])
    options = True
    while options:
        draw_tetromino([[0, 0], [1, 0], [0, 1], [1, 1]], 30, 110, (255, 255, 0), 0, 40, 170)
        draw_tetromino([[0, -2], [0, -1], [0, 0], [0, 1]], 120, 110, (71, 0, 178), 1, 120, 170)
        draw_tetromino([[-1, 0], [0, 0], [0, -1], [1, -1]], 200, 130, (255, 0, 0), 2, 200, 170)
        draw_tetromino([[-1, -1], [0, -1], [0, 0], [1, 0]], 300, 130, (0, 172, 23), 3, 300, 170)
        draw_tetromino([[0, -1], [0, 0], [0, 1], [1, 1]], 380, 110, (255, 133, 0), 4, 390, 170)
        draw_tetromino([[0, -1], [0, 0], [0, 1], [-1, 1]], 40, 230, (255, 133, 155), 5, 30, 280)
        draw_tetromino([[-1, 0], [0, 0], [1, 0], [0, -1]], 110, 250, (0, 255, 255), 6, 110, 280)
        draw_tetromino([[0, 0], [1, 0], [1, 1]], 180, 230, (114, 252, 64), 7, 190, 280)
        draw_tetromino([[-1, 0], [0, 0], [1, 0]], 270, 250, (186, 0, 155), 8, 270, 280)
        draw_tetromino([[0, 0], [1, 0]], 350, 250, (0, 94, 255), 9, 360, 280)
        draw_tetromino([[0, 0]], 420, 250, (128, 62, 0), 10, 420, 280)
        gameDisplay.blit(easy2, (38, 400))
        gameDisplay.blit(medium2, (185, 400))
        gameDisplay.blit(hard2, (332, 400))
        if difficulty == 0:
            gameDisplay.blit(easy1, (38, 400))
        if difficulty == 1:
            gameDisplay.blit(medium1, (185, 400))
        if difficulty == 2:
            gameDisplay.blit(hard1, (332, 400))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    position = pygame.mouse.get_pos()
                    if 35 < position[0] < 145 and 540 < position[1] < 570:
                        game_intro2()
                    if 4 < position[0] < 60 and 170 < position[1] < 190:
                        tetromines[0] = not tetromines[0]
                    if 120 < position[0] < 140 and 170 < position[1] < 190:
                        tetromines[1] = not tetromines[1]
                    if 200 < position[0] < 220 and 170 < position[1] < 190:
                        tetromines[2] = not tetromines[2]
                    if 300 < position[0] < 320 and 170 < position[1] < 190:
                        tetromines[3] = not tetromines[3]
                    if 390 < position[0] < 410 and 170 < position[1] < 190:
                        tetromines[4] = not tetromines[4]
                    if 30 < position[0] < 50 and 280 < position[1] < 300:
                        tetromines[5] = not tetromines[5]
                    if 110 < position[0] < 130 and 280 < position[1] < 300:
                        tetromines[6] = not tetromines[6]
                    if 190 < position[0] < 210 and 280 < position[1] < 300:
                        tetromines[7] = not tetromines[7]
                    if 270 < position[0] < 290 and 280 < position[1] < 300:
                        tetromines[8] = not tetromines[8]
                    if 360 < position[0] < 380 and 280 < position[1] < 300:
                        tetromines[9] = not tetromines[9]
                    if 420 < position[0] < 440 and 280 < position[1] < 300:
                        tetromines[10] = not tetromines[10]
                    if 38 < position[0] < 148 and 400 < position[1] < 430:
                        difficulty = 0
                    if 185 < position[0] < 295 and 400 < position[1] < 430:
                        difficulty = 1
                    if 332 < position[0] < 442 and 400 < position[1] < 430:
                        difficulty = 2
                    if 38 < position[0] < 200 and 475 < position[1] < 500:
                        left_controls()
                    if 270 < position[0] < 420 and 475 < position[1] < 500:
                        right_controls()

        position = pygame.mouse.get_pos()
        gameDisplay.blit(back, (35, 540))
        if 35 < position[0] < 145 and 540 < position[1] < 570:
            gameDisplay.blit(back2, (35, 540))
        pygame.display.update()
        CLOCK.tick(FPS)


def highscore():
    highscore = True
    level = difficulty
    while highscore:
        gameDisplay.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    position = pygame.mouse.get_pos()
                    if 35 < position[0] < 145 and 540 < position[1] < 570:
                        highscore = False
                        game_intro2()
                    if 38 < position[0] < 148 and 90 < position[1] < 120:
                        level = 0
                    if 185 < position[0] < 295 and 90 < position[1] < 120:
                        level = 1
                    if 332 < position[0] < 442 and 90 < position[1] < 120:
                        level = 2

        gameDisplay.blit(easy2, (38, 90))
        gameDisplay.blit(medium2, (185, 90))
        gameDisplay.blit(hard2, (332, 90))
        if level == 0:
            gameDisplay.blit(easy1, (38, 90))
            h = open("high1.txt", "r")
            for i in range(10):
                s = str(h.readline())
                s = s[:-1]
                highfont = pygame.font.SysFont("monospace", 20)
                text = highfont.render(s, True, (255, 255, 255))
                gameDisplay.blit(text, [170, 150 + 30 * i])
            h.close()
        if level == 1:
            gameDisplay.blit(medium1, (185, 90))
            h = open("high2.txt", "r")
            for i in range(10):
                s = str(h.readline())
                s = s[:-1]
                highfont = pygame.font.SysFont("monospace", 20)
                text = highfont.render(s, True, (255, 255, 255))
                gameDisplay.blit(text, [170, 150 + 30 * i])
            h.close()
        if level == 2:
            gameDisplay.blit(hard1, (332, 90))
            h = open("high3.txt", "r")
            for i in range(10):
                s = str(h.readline())
                s = s[:-1]
                highfont = pygame.font.SysFont("monospace", 20)
                text = highfont.render(s, True, (255, 255, 255))
                gameDisplay.blit(text, [170, 150 + 30 * i])
            h.close()

        gameDisplay.blit(highscore3, (160, 10))
        position = pygame.mouse.get_pos()
        gameDisplay.blit(back, (35, 540))
        if 35 < position[0] < 145 and 540 < position[1] < 570:
            gameDisplay.blit(back2, (35, 540))
        pygame.display.update()
        CLOCK.tick(FPS)


def draw_tetromino(squares, width, height, color, i, width2, height2):
    for square in squares:
        pygame.draw.rect(gameDisplay, (255, 255, 255),
                         [width + square[0] * BLOCK_SIZE2, height + square[1] * BLOCK_SIZE2, BLOCK_SIZE2, BLOCK_SIZE2])
        pygame.draw.rect(gameDisplay, color,
                         [width + 2 + square[0] * BLOCK_SIZE2, height + 2 + square[1] * BLOCK_SIZE2, BLOCK_SIZE2 - 4,
                          BLOCK_SIZE2 - 4])
    gameDisplay.blit(tic, (width2, height2))
    if tetromines[i] == True:
        gameDisplay.blit(tic2, (width2, height2))


def check_highscore(score):
    if tetromines == [True, True, True, True, True, True, True, False, False, False, False] and difficulty == 0:
        h = open("high1.txt", "r")
        for i in range(10):
            s = str(h.readline())
        found = int(re.search('\.\ .*\ ([0-9]*)', s).group(1))
        if score > found:
            add_highscore1(score)
        h.close()
    if tetromines == [True, True, True, True, True, True, True, False, False, False, False] and difficulty == 1:
        h = open("high2.txt", "r")
        for i in range(10):
            s = str(h.readline())
        found = int(re.search('\.\ .*\ ([0-9]*)', s).group(1))
        if score > found:
            add_highscore2(score)
        h.close()
    if tetromines == [True, True, True, True, True, True, True, False, False, False, False] and difficulty == 2:
        h = open("high3.txt", "r")
        for i in range(10):
            s = str(h.readline())
        found = int(re.search('\.\ .*\ ([0-9]*)', s).group(1))
        if score > found:
            add_highscore3(score)
        h.close()


def add_highscore1(score):
    name = get_name(score)
    h = open("high1.txt", "r")
    tab = [None for _ in range(10)]
    for i in range(10):
        tab[i] = str(h.readline())[2:]
    for i in range(9, -1, -1):
        try:
            x = int(re.search('\.\ .*\ ([0-9]*)', tab[i]).group(1))
        except AttributeError:
            x = 0
        if score > x:
            here = i
    h.close()
    tab.insert(here, ". " + name + " " + str(score) + "\n")
    h = open("high1.txt", "w")
    for i in range(9):
        h.write("0" + str(i + 1) + tab[i])
    h.write("10" + tab[9])
    h.close()
    highscore()


def add_highscore2(score):
    name = get_name(score)
    h = open("high2.txt", "r")
    tab = [None for _ in range(10)]
    for i in range(10):
        tab[i] = str(h.readline())[2:]
    for i in range(9, -1, -1):
        try:
            x = int(re.search('\.\ .*\ ([0-9]*)', tab[i]).group(1))
        except AttributeError:
            x = 0
        if score > x:
            here = i
    h.close()
    tab.insert(here, ". " + name + " " + str(score) + "\n")
    h = open("high2.txt", "w")
    for i in range(9):
        h.write("0" + str(i + 1) + tab[i])
    h.write("10" + tab[9])
    h.close()
    highscore()


def add_highscore3(score):
    name = get_name(score)
    h = open("high3.txt", "r")
    tab = [None for _ in range(10)]
    for i in range(10):
        tab[i] = str(h.readline())[2:]
    for i in range(9, -1, -1):
        try:
            x = int(re.search('\.\ .*\ ([0-9]*)', tab[i]).group(1))
        except AttributeError:
            x = 0
        if score > x:
            here = i
    h.close()
    tab.insert(here, ". " + name + " " + str(score) + "\n")
    h = open("high3.txt", "w")
    for i in range(9):
        h.write("0" + str(i + 1) + tab[i])
    h.write("10" + tab[9])
    h.close()
    highscore()


def get_name(score):
    get_name = True
    name = ''
    while get_name:
        gameDisplay.fill((0, 0, 0))
        gameDisplay.blit(my_font.render(str(score), True, white), [200, 70])
        gameDisplay.blit(highscore3, (160, 10))
        pygame.draw.rect(gameDisplay, (255, 255, 255), [60, 120, 360, 200])
        pygame.draw.rect(gameDisplay, (133, 133, 133), [65, 125, 350, 190])
        pygame.draw.rect(gameDisplay, (0, 0, 0), [70, 130, 340, 180])
        font_1 = pygame.font.SysFont("monospace", 30)
        text = font_1.render("Enter your name", True, (255, 255, 255))
        gameDisplay.blit(text, [110, 140])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    get_name = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
        name_surface = font_1.render(name, True, (255, 255, 255))
        gameDisplay.blit(name_surface, [160, 200])
        pygame.display.update()
        CLOCK.tick(FPS)

    return name


def game_exit():
    pygame.quit()
    exit(1)


def text_object(text, color, font):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, font):
    textSurf, textRect = text_object(msg, color, font)
    textRect.center = (MAP_WIDTH / 2), (MAP_HEIGHT / 2)
    gameDisplay.blit(textSurf, textRect)


def message(size, text, color, place):
    temporaryfont = pygame.font.SysFont("comicsansms", size)
    texty = temporaryfont.render(text, True, color)
    gameDisplay.blit(texty, place)


font = pygame.font.SysFont(None, 15)
font2 = pygame.font.SysFont(None, 3)


def GameLoop():
    global score
    global exist
    global game_over
    block_grid = []
    for _ in range(20):
        block_grid.append([None for _ in range(10)])

    tet = Tetromino()
    tet2 = Tetromino()
    tet2.generate()
    tet.generate()
    exist = True
    count = 1
    game_over = False
    score = 0
    level = 1

    while True:
        if exist is False:
            tet.color = tet2.color
            tet.pos = tet2.pos
            tet.squares = tet2.squares
            tet2.generate()
            tet.is_it_game_over(block_grid)
        if game_over:
            game = False
            check_highscore(score)
            while not game:
                gameDisplay.fill((0, 0, 0))
                gameDisplay.blit(game_over1, (40, 100))
                position = pygame.mouse.get_pos()
                gameDisplay.blit(play_again1, (87, 250))
                if 87 < position[0] < 197 and 250 < position[1] < 280:
                    gameDisplay.blit(play_again2, (87, 250))
                gameDisplay.blit(main_menu1, (283, 250))
                if 283 < position[0] < 393 and 250 < position[1] < 280:
                    gameDisplay.blit(main_menu2, (283, 250))
                gameDisplay.blit(quit1, (35, 540))
                if 35 < position[0] < 145 and 540 < position[1] < 570:
                    gameDisplay.blit(quit2, (35, 540))

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_exit()
                        if event.key == pygame.K_c:
                            game_over = False
                            game = True
                            GameLoop()
                        if event.key == pygame.K_m:
                            game_over = False
                            game_intro2()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if 87 < position[0] < 197 and 250 < position[1] < 280:
                            game_over = False
                            GameLoop()
                        if 283 < position[0] < 393 and 250 < position[1] < 280:
                            game_over = False
                            game_intro2()
                        if 35 < position[0] < 145 and 540 < position[1] < 570:
                            game_exit()

        if count % (falling_speed[difficulty + level - 1]) == 0:
            tet.move_down(block_grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == rp_left:
                    if tet.can_go_left(block_grid) is True:
                        tet.move_horizontal(-1)
                if event.key == rp_right:
                    if tet.can_go_right(block_grid) is True:
                        tet.move_horizontal(1)
                if event.key == rp_up:
                    tet.rotate(block_grid)
                if event.key == rp_down:
                    tet.move_down(block_grid)
                if event.key == rp_drop:
                    tet.drop(block_grid)
                elif event.key == pygame.K_p:
                    pause()
        for line in range(20):
            to_eliminate = True
            for column in range(10):
                if block_grid[line][column] is None:
                    to_eliminate = False
            if to_eliminate is True:
                block_grid.pop(line)
                block_grid.insert(0, [None for _ in range(10)])
                score += 10
                if score % 100 == 0 and level <= 9:
                    level += 1

        gameDisplay.fill((0, 0, 0))
        pygame.draw.rect(gameDisplay, (255, 255, 255), [2, 2, 300, 600])
        # teraz rysujemy block grid
        for line in range(20):
            column = 0
            for bl in block_grid[line]:  # iteruj po polach w linii block grida
                if bl is not None:  # jeżeli jest tam zapisany jakiś kolor (nazwany tutaj "bl")
                    pygame.draw.rect(gameDisplay, (0, 0, 0),
                                     [column * BLOCK_SIZE + 2, line * BLOCK_SIZE + 2, BLOCK_SIZE,
                                      BLOCK_SIZE])  # narysuj czarny kwadrat
                    pygame.draw.rect(gameDisplay, bl, [column * 30 + 4, line * 30 + 4, BLOCK_SIZE - 4,
                                                       BLOCK_SIZE - 4])  # w środku narysuj kwadrat o zadanym kolorze

                column += 1

            # teraz rysujemy spadający klocek

        for square in tet.squares:  # dla każdego kwadraciku
            # narysuj czarny kwadrat
            pygame.draw.rect(gameDisplay, (0, 0, 0), [tet.pos[0] * BLOCK_SIZE + 2 + square[0] * BLOCK_SIZE,
                                                      tet.pos[1] * BLOCK_SIZE + 2 + square[1] * BLOCK_SIZE, BLOCK_SIZE,
                                                      BLOCK_SIZE])
            # w środku narysuj kwadrat o kolorze klocka
            pygame.draw.rect(gameDisplay, tet.color, [tet.pos[0] * BLOCK_SIZE + 4 + square[0] * BLOCK_SIZE,
                                                      tet.pos[1] * BLOCK_SIZE + 4 + square[1] * BLOCK_SIZE,
                                                      BLOCK_SIZE - 4, BLOCK_SIZE - 4])

        myfont = pygame.font.SysFont("monospace", 20)
        text = myfont.render("Score = " + str(score), True, (255, 255, 255))
        gameDisplay.blit(text, [324, 250])
        text2 = myfont.render("Level " + str(level), True, (255, 255, 255))
        gameDisplay.blit(text2, [324, 220])

        pygame.draw.rect(gameDisplay, (255, 255, 255), [317, 10, 150, 180])
        for square in tet2.squares:
            pygame.draw.rect(gameDisplay, (0, 0, 0), [tet2.pos[0] * BLOCK_SIZE + 2 + square[0] * BLOCK_SIZE + 257,
                                                      tet2.pos[1] * BLOCK_SIZE + 2 + square[1] * BLOCK_SIZE + 30,
                                                      BLOCK_SIZE, BLOCK_SIZE])

        pygame.display.update()
        CLOCK.tick(FPS)
        count += 1


def GameLoop2():
    global left_score
    global right_score
    global left_exist
    global right_exist
    global game_over
    global level

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
    l_tet = Tetromino()
    l_tet.generate()
    r_tet = copy.deepcopy(l_tet)
    tet2 = Tetromino()
    tet2.generate()
    left_exist = True
    right_exist = True
    game_over = False
    count = 1
    left_score = 0
    right_score = 0
    level = 1

    while True:
        if left_exist and right_exist:
            speed = falling_speed[difficulty + level - 1]
        else:
            speed = falling_speed[difficulty + level + 2]
        if left_exist is False and right_exist is False:
            l_tet = copy.deepcopy(tet2)
            r_tet = copy.deepcopy(tet2)
            tet2.generate2()
            l_tet.is_it_game_over(left_block_grid)
            r_tet.is_it_game_over(right_block_grid)

        if game_over:
            game = False
            while not game:
                game_display.fill((0, 0, 0))
                game_display.blit(game_over1, (40, 100))
                position = pygame.mouse.get_pos()
                game_display.blit(play_again1, (87, 250))
                if 87 < position[0] < 197 and 250 < position[1] < 280:
                    game_display.blit(play_again2, (87, 250))
                game_display.blit(main_menu1, (283, 250))
                if 283 < position[0] < 393 and 250 < position[1] < 280:
                    game_display.blit(main_menu2, (283, 250))
                game_display.blit(quit1, (35, 540))
                if 35 < position[0] < 145 and 540 < position[1] < 570:
                    game_display.blit(quit2, (35, 540))

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_exit()
                        if event.key == pygame.K_c:
                            game_over = False
                            game = True
                            GameLoop2()
                        if event.key == pygame.K_m:
                            game_over = False
                            game_intro2()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if 87 < position[0] < 197 and 250 < position[1] < 280:
                            game_over = False
                            GameLoop2()
                        if 283 < position[0] < 393 and 250 < position[1] < 280:
                            game_over = False
                            game_intro2()
                        if 35 < position[0] < 145 and 540 < position[1] < 570:
                            game_exit()

        if count % speed == 0:
            if left_exist:
                l_tet.move_down2(left_block_grid, middle_block_grid, False)
            if right_exist:
                r_tet.move_down2(right_block_grid, middle_block_grid, True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == rp_left:
                    if r_tet.can_right_go_left(right_block_grid, middle_block_grid, l_tet) is True:
                        r_tet.move_horizontal(-1)
                if event.key == lp_left:
                    if l_tet.can_go_left(left_block_grid) is True:
                        l_tet.move_horizontal(-1)
                if event.key == rp_right:
                    if r_tet.can_go_right(right_block_grid) is True:
                        r_tet.move_horizontal(1)
                if event.key == lp_right:
                    if l_tet.can_left_go_right(left_block_grid, middle_block_grid, r_tet):
                        l_tet.move_horizontal(1)
                if event.key == rp_up:
                    r_tet.rotate(right_block_grid)
                if event.key == lp_up:
                    l_tet.rotate(left_block_grid)
                if event.key == rp_down:
                    r_tet.move_down2(right_block_grid, middle_block_grid, True)
                if event.key == lp_down:
                    l_tet.move_down2(left_block_grid, middle_block_grid, False)
                if event.key == rp_drop:
                    r_tet.drop2(right_block_grid, middle_block_grid, True)
                if event.key == lp_drop:
                    l_tet.drop2(left_block_grid, middle_block_grid, False)
                elif event.key == pygame.K_p:
                    pause()
        # for line in range(20):
        #     to_eliminate = True
        #     for column in range(10):
        #         if right_block_grid[line][column] is None:
        #             to_eliminate = False
        #     if to_eliminate is True:
        #         right_block_grid.pop(line)
        #         right_block_grid.insert(0, [None for _ in range(10)])
        #         middle_block_grid.pop(line)
        #         middle_block_grid.insert(0, [None])
        #         right_score += 5
        #         if (right_score + left_score) % 100 == 0:
        #             level += 1
        #
        #     to_eliminate = True
        #     for column in range(10):
        #         if left_block_grid[line][column] is None:
        #             to_eliminate = False
        #     if to_eliminate is True:
        #         left_block_grid.pop(line)
        #         left_block_grid.insert(0, [None for _ in range(10)])
        #         middle_block_grid.pop(line)
        #         middle_block_grid.insert(0, [None])
        #         left_score += 5
        #         if (right_score + left_score) % 100 == 0:
        #             level += 1

        game_display.fill((0, 0, 0))
        pygame.draw.rect(game_display, (255, 255, 255), [180, 2, 21 * BLOCK_SIZE, 20 * BLOCK_SIZE])
        pygame.draw.rect(game_display, (200, 200, 200), [180 + 10 * BLOCK_SIZE, 2, BLOCK_SIZE, 20 * BLOCK_SIZE])
        # teraz rysujemy prawy block grid
        for line in range(20):
            column = 0
            for color in right_block_grid[line]:
                if color is not None:
                    pygame.draw.rect(game_display, (0, 0, 0),
                                     [180 + 11 * BLOCK_SIZE + column * BLOCK_SIZE, line * BLOCK_SIZE + 2, BLOCK_SIZE,
                                      BLOCK_SIZE])
                    pygame.draw.rect(game_display, color,
                                     [180 + 11 * BLOCK_SIZE + column * BLOCK_SIZE + 2, line * BLOCK_SIZE + 4,
                                      BLOCK_SIZE - 4,
                                      BLOCK_SIZE - 4])
                column += 1

        for line in range(20):
            column = 0
            for color in left_block_grid[line]:
                if color is not None:
                    pygame.draw.rect(game_display, (0, 0, 0),
                                     [180 + column * BLOCK_SIZE, line * BLOCK_SIZE + 2, BLOCK_SIZE,
                                      BLOCK_SIZE])
                    pygame.draw.rect(game_display, color,
                                     [180 + column * BLOCK_SIZE + 2, line * BLOCK_SIZE + 4, BLOCK_SIZE - 4,
                                      BLOCK_SIZE - 4])
                column += 1

        for line in range(20):
            for color in middle_block_grid[line]:  # iteruj po polach w linii block grida
                if color is not None:  # jeżeli jest tam zapisany jakiś kolor
                    pygame.draw.rect(game_display, (0, 0, 0),
                                     [180 + 10 * BLOCK_SIZE, line * BLOCK_SIZE + 2, BLOCK_SIZE,
                                      BLOCK_SIZE])  # narysuj czarny kwadrat
                    pygame.draw.rect(game_display, color,
                                     [180 + 10 * BLOCK_SIZE + 2, line * BLOCK_SIZE + 4, BLOCK_SIZE - 4,
                                      BLOCK_SIZE - 4])  # w środku narysuj kwadrat o zadanym kolorze

        # teraz rysujemy spadający klocek
        if right_exist:
            for square in r_tet.squares:
                # narysuj czarny kwadrat
                pygame.draw.rect(game_display, (0, 0, 0),
                                 [180 + 11 * BLOCK_SIZE + r_tet.pos[0] * BLOCK_SIZE + square[0] * BLOCK_SIZE,
                                  r_tet.pos[1] * BLOCK_SIZE + 2 + square[1] * BLOCK_SIZE, BLOCK_SIZE,
                                  BLOCK_SIZE])
                # w środku narysuj kwadrat o kolorze klocka
                pygame.draw.rect(game_display, r_tet.color,
                                 [180 + 11 * BLOCK_SIZE + r_tet.pos[0] * BLOCK_SIZE + 2 + square[0] * BLOCK_SIZE,
                                  r_tet.pos[1] * BLOCK_SIZE + 4 + square[1] * BLOCK_SIZE,
                                  BLOCK_SIZE - 4, BLOCK_SIZE - 4])

        if left_exist:
            for square in l_tet.squares:
                pygame.draw.rect(game_display, (0, 0, 0),
                                 [180 + l_tet.pos[0] * BLOCK_SIZE + square[0] * BLOCK_SIZE,
                                  l_tet.pos[1] * BLOCK_SIZE + 2 + square[1] * BLOCK_SIZE, BLOCK_SIZE,
                                  BLOCK_SIZE])
                pygame.draw.rect(game_display, l_tet.color,
                                 [180 + l_tet.pos[0] * BLOCK_SIZE + 2 + square[0] * BLOCK_SIZE,
                                  l_tet.pos[1] * BLOCK_SIZE + 4 + square[1] * BLOCK_SIZE,
                                  BLOCK_SIZE - 4, BLOCK_SIZE - 4])

        text = my_font.render("Score = " + str(left_score), True, (255, 255, 255))
        game_display.blit(text, [24, 250])
        text2 = my_font.render("Level " + str(level), True, (255, 255, 255))
        game_display.blit(text2, [24, 220])
        text3 = my_font.render("Score = " + str(right_score), True, (255, 255, 255))
        gameDisplay.blit(text3, [834, 250])
        game_display.blit(text2, [834, 220])

        pygame.draw.rect(game_display, (255, 255, 255), [17, 10, 150, 180])
        pygame.draw.rect(game_display, (255, 255, 255), [827, 10, 150, 180])
        for square in tet2.squares:
            pygame.draw.rect(game_display, (0, 0, 0), [tet2.pos[0] * BLOCK_SIZE + 2 + square[0] * BLOCK_SIZE - 43,
                                                       tet2.pos[1] * BLOCK_SIZE + 2 + square[1] * BLOCK_SIZE + 30,
                                                       BLOCK_SIZE, BLOCK_SIZE])
            pygame.draw.rect(game_display, (0, 0, 0), [tet2.pos[0] * BLOCK_SIZE + 2 + square[0] * BLOCK_SIZE + 767,
                                                       tet2.pos[1] * BLOCK_SIZE + 2 + square[1] * BLOCK_SIZE + 30,
                                                       BLOCK_SIZE, BLOCK_SIZE])

        pygame.display.update()
        CLOCK.tick(FPS)
        count += 1


gameDisplay = pygame.display.set_mode(MAP_SIZE)
pygame.display.set_caption("Best Tetris")
gameDisplay.fill((255, 255, 255))
pygame.display.update()

game_intro2()
