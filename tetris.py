import pygame
import random

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS

S_ = [[0, 0, 0, 0,
       0, 1, 1, 0,
       1, 1, 0, 0,
       0, 0, 0, 0],
      [0, 1, 0, 0,
       0, 1, 1, 0,
       0, 0, 1, 0,
       0, 0, 0, 0],
      [0, 0, 0, 0,
       0, 1, 1, 0,
       1, 1, 0, 0,
       0, 0, 0, 0],
      [0, 1, 0, 0,
       0, 1, 1, 0,
       0, 0, 1, 0,
       0, 0, 0, 0]]

Z_ = [[0, 0, 0, 0,
       1, 1, 0, 0,
       0, 1, 1, 0,
       0, 0, 0, 0],
      [0, 0, 1, 0,
       0, 1, 1, 0,
       0, 1, 0, 0,
       0, 0, 0, 0],
      [0, 0, 0, 0,
       1, 1, 0, 0,
       0, 1, 1, 0,
       0, 0, 0, 0],
      [0, 0, 1, 0,
       0, 1, 1, 0,
       0, 1, 0, 0,
       0, 0, 0, 0]]

I_ = [[0, 0, 0, 0,
       1, 1, 1, 1,
       0, 0, 0, 0,
       0, 0, 0, 0],
      [0, 0, 1, 0,
       0, 0, 1, 0,
       0, 0, 1, 0,
       0, 0, 1, 0],
      [0, 0, 0, 0,
       1, 1, 1, 1,
       0, 0, 0, 0,
       0, 0, 0, 0],
      [0, 0, 1, 0,
       0, 0, 1, 0,
       0, 0, 1, 0,
       0, 0, 1, 0]]

O_ = [[0, 0, 0, 0,
       0, 1, 1, 0,
       0, 1, 1, 0,
       0, 0, 0, 0],
      [0, 0, 0, 0,
       0, 1, 1, 0,
       0, 1, 1, 0,
       0, 0, 0, 0],
      [0, 0, 0, 0,
       0, 1, 1, 0,
       0, 1, 1, 0,
       0, 0, 0, 0],
      [0, 0, 0, 0,
       0, 1, 1, 0,
       0, 1, 1, 0,
       0, 0, 0, 0]]

J_ = [[0, 0, 0, 0,
       1, 1, 1, 0,
       0, 0, 1, 0,
       0, 0, 0, 0],
      [0, 1, 0, 0,
       0, 1, 0, 0,
       1, 1, 0, 0,
       0, 0, 0, 0],
      [1, 0, 0, 0,
       1, 1, 1, 0,
       0, 0, 0, 0,
       0, 0, 0, 0],
      [0, 1, 1, 0,
       0, 1, 0, 0,
       0, 1, 0, 0,
       0, 0, 0, 0]]

L_ = [[0, 0, 0, 0,
       1, 1, 1, 0,
       1, 0, 0, 0,
       0, 0, 0, 0],
      [1, 1, 0, 0,
       0, 1, 0, 0,
       0, 1, 0, 0,
       0, 0, 0, 0],
      [0, 0, 1, 0,
       1, 1, 1, 0,
       0, 0, 0, 0,
       0, 0, 0, 0],
      [0, 1, 0, 0,
       0, 1, 0, 0,
       0, 1, 1, 0,
       0, 0, 0, 0]]

T_ = [[0, 0, 0, 0,
       1, 1, 1, 0,
       0, 1, 0, 0,
       0, 0, 0, 0],
      [0, 1, 0, 0,
       1, 1, 0, 0,
       0, 1, 0, 0,
       0, 0, 0, 0],
      [0, 1, 0, 0,
       1, 1, 1, 0,
       0, 0, 0, 0,
       0, 0, 0, 0],
      [0, 1, 0, 0,
       0, 1, 1, 0,
       0, 1, 0, 0,
       0, 0, 0, 0]]

shapes = [S_, Z_, I_, O_, J_, L_, T_]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# index 0 - 6 represent shape



class Piece(object):  # *
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_pos={}):  # *
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []

    for y in range(4):
        for x in range(4):
            i = y * 4 + x

            if shape.shape[shape.rotation % 4][i] == 1:
                positions.append((shape.x + x - 2, shape.y + y - 4))

    # for i, pos in enumerate(positions):
    #    positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
            if pos[0] < 0 or pos[0] > 9:
                return False

    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def get_shape_i(i):
    return Piece(5, 0, shapes[int(i)%7])


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, True, color)

    surface.blit(label, (
    top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))


def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
            for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
                x, y = key
                #print(y)
                if y < i:
                    newKey = (x, y + 1)
                    locked[newKey] = locked.pop(key)

    return inc


def calculate_score(completed_lines, level):
    if completed_lines == 1:
        return 40 * (level + 1)
    elif completed_lines == 2:
        return 100 * (level + 1)
    elif completed_lines == 3:
        return 300 * (level + 1)
    elif completed_lines == 4:
        return 1200 * (level + 1)
    return 0


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    for i in range(4):
        for j in range(4):
            if shape.shape[0][i * 4 + j] == 1:
                pygame.draw.rect(surface, shape.color, (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def draw_window(surface, grid, score=0, last_score=0):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # current score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    surface.blit(label, (sx + 20, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid)
    # pygame.display.update()