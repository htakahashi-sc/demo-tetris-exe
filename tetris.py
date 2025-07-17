import pygame
import random

# 定数
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
PLAY_AREA_WIDTH = GRID_WIDTH * GRID_SIZE
PLAY_AREA_HEIGHT = GRID_HEIGHT * GRID_SIZE
PLAY_AREA_X = (SCREEN_WIDTH - PLAY_AREA_WIDTH) // 2
PLAY_AREA_Y = (SCREEN_HEIGHT - PLAY_AREA_HEIGHT)

# 色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# テトリミノの形状
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1], [1, 1]]   # O
]

# テトリミノの色
SHAPE_COLORS = [CYAN, RED, GREEN, PURPLE, ORANGE, BLUE, YELLOW]


class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0

    def draw(self, screen):
        for r, row in enumerate(self.shape):
            for c, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.color,
                                     (PLAY_AREA_X + self.x*GRID_SIZE + c * GRID_SIZE, PLAY_AREA_Y + self.y*GRID_SIZE + r * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
                    pygame.draw.rect(screen, WHITE,
                                     (PLAY_AREA_X + self.x*GRID_SIZE + c * GRID_SIZE, PLAY_AREA_Y + self.y*GRID_SIZE + r * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


def get_random_shape():
    return random.choice(SHAPES)

def draw_play_area(screen):
    pygame.draw.rect(screen, WHITE, (PLAY_AREA_X - 2, PLAY_AREA_Y - 2, PLAY_AREA_WIDTH + 4, PLAY_AREA_HEIGHT + 4), 2)

def create_grid(locked_positions={}):
    grid = [[(0,0,0) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if (x,y) in locked_positions:
                c = locked_positions[(x,y)]
                grid[y][x] = c
    return grid

def convert_shape_format(shape):
    positions = []
    for r, row in enumerate(shape.shape):
        for c, cell in enumerate(row):
            if cell:
                positions.append((shape.x + c, shape.y + r))
    return positions

def is_valid_position(shape, grid):
    formatted = convert_shape_format(shape)
    for x, y in formatted:
        if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
            return False
        if y >= 0 and grid[y][x] != (0,0,0):
            return False
    return True

def draw_grid(screen, grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(screen, grid[y][x], (PLAY_AREA_X + x*GRID_SIZE, PLAY_AREA_Y + y*GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
    draw_play_area(screen)

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def draw_text_middle(text, size, color, screen):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    screen.blit(label, (PLAY_AREA_X + PLAY_AREA_WIDTH/2 - (label.get_width()/2), PLAY_AREA_Y + PLAY_AREA_HEIGHT/2 - label.get_height()/2))

def draw_next_shape(shape, screen):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, WHITE)

    sx = PLAY_AREA_X + PLAY_AREA_WIDTH + 50
    sy = PLAY_AREA_Y + PLAY_AREA_HEIGHT/2 - 100

    for r, row in enumerate(shape.shape):
        for c, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, shape.color, (sx + c*GRID_SIZE, sy + r*GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

    screen.blit(label, (sx + 10, sy - 30))

def main():
    """ メインループ """
    locked_positions = {}
    grid = create_grid(locked_positions)

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("テトリス")

    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0

    current_tetromino = Tetromino(5, 0, get_random_shape())
    next_tetromino = Tetromino(5, 0, get_random_shape())
    change_piece = False
    run = True
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_tetromino.y += 1
            if not (is_valid_position(current_tetromino, grid)) and current_tetromino.y > 0:
                current_tetromino.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetromino.x -= 1
                    if not is_valid_position(current_tetromino, grid):
                        current_tetromino.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_tetromino.x += 1
                    if not is_valid_position(current_tetromino, grid):
                        current_tetromino.x -= 1
                elif event.key == pygame.K_UP:
                    current_tetromino.rotate()
                    if not is_valid_position(current_tetromino, grid):
                        current_tetromino.rotate()
                        current_tetromino.rotate()
                        current_tetromino.rotate()
                if event.key == pygame.K_DOWN:
                    current_tetromino.y += 1
                    if not is_valid_position(current_tetromino, grid):
                        current_tetromino.y -= 1

        shape_pos = convert_shape_format(current_tetromino)

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_tetromino.color
            current_tetromino = next_tetromino
            next_tetromino = Tetromino(5, 0, get_random_shape())
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        screen.fill(BLACK)
        draw_grid(screen, grid)
        current_tetromino.draw(screen)
        draw_next_shape(next_tetromino, screen)

        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Score: ' + str(score), 1, WHITE)
        sx = PLAY_AREA_X + PLAY_AREA_WIDTH + 50
        sy = PLAY_AREA_Y + PLAY_AREA_HEIGHT/2 - 100
        screen.blit(label, (sx + 10, sy + 160))

        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle("You Lost", 40, WHITE, screen)
            pygame.display.update()
            pygame.time.delay(2000)
            run = False

    pygame.quit()

if __name__ == '__main__':
    main()
