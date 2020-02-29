import random

import pygame

# initiate pygame & display
pygame.init()
clock = pygame.time.Clock()
FPS = 3
cube_size = 40  # int(input('Please Enter cube size 20~40: '))
grid_count = 10  # int(input('Please Enter grid count 10~20: '))
screen_size = ((cube_size + 1) * grid_count) + 1
screen = pygame.display.set_mode((screen_size, screen_size))
screen.fill((255, 255, 255))

curr_direction = 'UP'

font = pygame.font.Font('freesansbold.ttf', int(12 * grid_count * cube_size / 400) + 4)
over_font = pygame.font.Font('freesansbold.ttf', int(24 * grid_count * cube_size / 400) + 8)


class Cube:
    def __init__(self, x, y):
        self.x_pos = x
        self.x_mov = 0
        self.y_pos = y
        self.y_mov = 0
        self.rect = pygame.Rect(int(x * (cube_size + 1) + 1), int(y * (cube_size + 1) + 1), cube_size, cube_size)
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def move(self, new_direction):
        if new_direction == 'UP':
            if self.y_pos <= 0:
                self.y_mov = (cube_size + 1) * (grid_count - 1)
                self.y_pos = grid_count - 1
            else:
                self.y_mov = - (cube_size + 1)
                self.y_pos -= 1
            self.x_mov = 0
            # print(f'{new_direction} --- ( {self.x_pos} | {self.y_pos} ) --- ( {self.x_mov} | {self.y_mov} )')
        elif new_direction == 'RIGHT':
            if self.x_pos >= grid_count - 1:
                self.x_mov = -(cube_size + 1) * (grid_count - 1)
                self.x_pos = 0
            else:
                self.x_mov = (cube_size + 1)
                self.x_pos += 1
            self.y_mov = 0
            # print(f'{new_direction} --- ( {self.x_pos} | {self.y_pos} ) --- ( {self.x_mov} | {self.y_mov} )')
        elif new_direction == 'DOWN':
            if self.y_pos >= grid_count - 1:
                self.y_mov = -(cube_size + 1) * (grid_count - 1)
                self.y_pos = 0
            else:
                self.y_mov = (cube_size + 1)
                self.y_pos += 1
            self.x_mov = 0
            # print(f'{new_direction} --- ( {self.x_pos} | {self.y_pos} ) --- ( {self.x_mov} | {self.y_mov} )')
        elif new_direction == 'LEFT':
            if self.x_pos <= 0:
                self.x_mov = (cube_size + 1) * (grid_count - 1)
                self.x_pos = grid_count - 1
            else:
                self.x_mov = - (cube_size + 1)
                self.x_pos -= 1
            self.y_mov = 0
            # print(f'{new_direction} --- ( {self.x_pos} | {self.y_pos} ) --- ( {self.x_mov} | {self.y_mov} )')
        else:
            self.x_mov = 0
            self.y_mov = 0
            # print(f'{new_direction} --- ( {self.x_pos} | {self.y_pos} ) --- ( {self.x_mov} | {self.y_mov} )')

    def draw(self):
        self.rect.move_ip((self.x_mov, self.y_mov))
        pygame.draw.rect(screen, (255, 0, 0), self.rect)


class Snake:
    def __init__(self):
        self.cubes = [Cube((grid_count / 2), (grid_count / 2)), Cube((grid_count / 2), (grid_count / 2) + 1),
                      Cube((grid_count / 2), (grid_count / 2) + 2)]
        self.directions = ['UP', 'UP', 'UP']
        self.x, self.y = (grid_count / 2), (grid_count / 2) + 2

    def move(self, new_direction):
        global sx, sy
        self.x, self.y = self.cubes[-1].x_pos, self.cubes[-1].y_pos

        # print(f'( {self.x} | {self.y} )\n')

        for i in range(len(self.cubes)):
            if (len(self.cubes) - 1 - i) == 0:
                self.directions[len(self.cubes) - 1 - i] = new_direction
            else:
                self.directions[len(self.cubes) - 1 - i] = self.directions[len(self.cubes) - 2 - i]
        for i in range(len(self.cubes)):
            self.cubes[i].move(self.directions[i])

        if self.cubes[0].x_pos == sx and self.cubes[0].y_pos == sy:
            self.add_cube()
            snack_replace()

    def reset(self):
        self.cubes = [Cube((grid_count / 2), (grid_count / 2)), Cube((grid_count / 2), (grid_count / 2) + 1),
                      Cube((grid_count / 2), (grid_count / 2) + 2)]
        self.directions = ['UP', 'UP', 'UP']
        self.x, self.y = (grid_count / 2), (grid_count / 2) + 2

    def add_cube(self):
        self.cubes.append(Cube(self.x, self.y))
        self.directions.append('NONE')

    def draw(self):
        for cube in self.cubes:
            cube.draw()

    def check_collision(self):
        for ocube in self.cubes:
            for icube in self.cubes:
                if ocube != icube:
                    if ocube.x_pos == icube.x_pos and ocube.y_pos == icube.y_pos:
                        #print(f'{ocube} and {icube} are at the same position ( {ocube.x_pos} | {ocube.y_pos} ) - ( {icube.x_pos} | {icube.y_pos} )')
                        return True
        return False


def draw_grid():
    for x in range(grid_count):
        for y in range(grid_count):
            rect = pygame.Rect(x * (cube_size + 1) + 1, y * (cube_size + 1) + 1, cube_size, cube_size)
            pygame.draw.rect(screen, (0, 0, 0), rect)


def random_snack():
    repeat = True
    while repeat:
        c = 0

        x = random.randint(0, grid_count - 1)
        y = random.randint(0, grid_count - 1)

        for cube in snake.cubes:
            if x == cube.x_pos and y == cube.y_pos:
                c += 1
        if c == 0:
            repeat = False

    print(f'New snack at ( {x} | {y} )')
    return x, y


def snack_replace():
    global sx, sy
    dx, dy = random_snack()
    snack.move_ip((dx - sx) * (cube_size + 1), (dy - sy) * (cube_size + 1))
    sx = dx
    sy = dy


def redraw_window(s):
    if not game_over:
        screen.fill((255, 255, 255))
        draw_grid()
        pygame.draw.rect(screen, (0, 255, 0), s)
        snake.draw()
    if game_over:
        screen.fill((255, 255, 255))
        show_gameover()
    pygame.display.update()


def show_gameover():
    over_text1 = over_font.render('GAME OVER', True, (0, 0, 0))
    screen.blit(over_text1, (int((screen_size / 2) - (over_text1.get_rect().width / 2)),
                             int((screen_size / 2) - (over_text1.get_rect().height / 2))))
    over_text2 = font.render('PRESS ENTER TO START NEW GAME', True, (0, 0, 0))
    screen.blit(over_text2, (int((screen_size / 2) - (over_text2.get_rect().width / 2)),
                             int((screen_size / 2) + (over_text1.get_rect().height / 2) + 10)))
    over_text3 = font.render(f'Maximum Length: {len(snake.cubes)}', True, (0, 0, 0))
    screen.blit(over_text3, (int((screen_size / 2) - (over_text3.get_rect().width / 2)), int(
        (screen_size / 2) - (over_text1.get_rect().height / 2) - over_text3.get_rect().height - 10)))


def check_event(event, run, g_over, direction):
    if event.type == pygame.QUIT:
        run = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_KP8:
            #print('going up')
            direction = 'UP'
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_KP6:
            #print('going right')
            direction = 'RIGHT'
        if event.key == pygame.K_DOWN or event.key == pygame.K_s or event.key == pygame.K_KP2:
            #print('going down')
            direction = 'DOWN'
        if event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_KP4:
            #print('going left')
            direction = 'LEFT'
        if event.key == pygame.K_RETURN and g_over:
            g_over = False
            direction = 'UP'
            snake.reset()
            snack_replace()

    return run, g_over, direction


# Initiate Snake and Snack
snake = Snake()
sx, sy = random_snack()
snack = pygame.Rect(sx * (cube_size + 1) + 1, sy * (cube_size + 1) + 1, cube_size, cube_size)

# game loop
running = True
game_over = False
while running:
    clock.tick(FPS)

    # event check
    for e in pygame.event.get():
        running, game_over, curr_direction = check_event(e, running, game_over, curr_direction)

    if not game_over:
        # move cube
        snake.move(new_direction=curr_direction)

        # check game over
        game_over = snake.check_collision()

    # update display
    redraw_window(snack)
