# https://www.askforgametask.com/tutorial/machine-learning/ai-plays-tetris-with-cnn/
# https://www.techwithtim.net/tutorials/game-development-with-python/tetris-pygame/tutorial-1/
# https://www.youtube.com/watch?v=wQWWzBHUJWM&ab_channel=TechWithTim

import pygame
import random
import neat
import numpy
import pickle

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
    ind = -1
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
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

def get_input(grid,current_piece, next_piece):
    _input = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == (0, 0, 0,):
                _input.append(0)
            else:
                _input.append(1)

    for val in current_piece.shape[0]:
        _input.append(val)

    for val in next_piece.shape[0]:
        _input.append(val)

    return _input


def get_output(net, grid, current_piece, next_piece):
    _input = get_input(grid, current_piece, next_piece)
    _output = net.activate(_input)

    #wersja dla 2 wejść, gdzie pierwsza wartość oznacza kolumnę (0.0-1.0 -> 0-9)
    #                          druga wartość oznacza rotację (0.0-1.0 -> 0-3)
    rotation = int(_output[1] * 4)
    if rotation == 4:
        rotation -= 1
    position = int(_output[0] * 10)

    return position, rotation

    # wersja dla 40 wyjść, gdzie każdy output oznacza inną kombinację kolumny i rotacji dla danego tetrimino
    #best_index = _output.index(max(_output))

    #return best_index % 10, best_index // 10

def calculate_fitness(score, level, lines, locked):
    # obliczanie fitnesu
    cleared = level * 10 + lines
    fitness = 0
    if cleared > 0:
        fitness += score / cleared

        # bonus za każdą linię
        fitness += 10 * cleared / score


    holes = 0.05 # kara za dziury
    highest_block_y = 0 # jak wysoko jesteśmy zbudowani
    hole_depth = [0] * 10 # głębokość nierówności
    for y in range(20):
        y = 19 - y #skanujemy od dołu
        found_block = False
        block_length = 0
        for x in range(10): #skanujemy od lewej strony
            #znajdowanie dziur w ułożonym bloku
            if (x,y) not in locked:
                if (x,y-1) in locked:
                    fitness -= holes
                block_length = 0
                # sprawdzanie nierówności:
                hole_depth[x] += 1
            else:
                #fitness -= 0.01 * hole_depth[x]
                hole_depth[x] = 0
                block_length += 1
                fitness += 0.01/(y+1) * block_length
                found_block = True
        if found_block:
            highest_block_y += 1
        else:
            hole_depth = [x + highest_block_y - 20 for x in hole_depth]
            break
    #chcemy mieć wysokość do 4
    if highest_block_y <= 4:
        fitness += 0.5 * highest_block_y
    else:
        fitness -= 3 * (highest_block_y - 4)
    # chcemy płaską powierzchnię (nie więcej niż dwa głębokości)
    for depth in hole_depth:
        if depth > 2:
            fitness -= 0.05 * depth
        else:
            fitness -= 0.01

    return fitness


def evaluate_genome(genomes, config):
    # pętla po wszystkich osobnikach w naszej populacji
    for genome_id, genome in genomes:
        win = pygame.display.set_mode((s_width, s_height))
        pygame.display.set_caption('Tetris')
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        main(win, net, genome)
        pygame.display.quit()


def main(win, net = None, genome = None):  # *
    #zaczyna się gra
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.02 #0.02
    score = 0
    lines = 0
    level = 0
    use_nn = True

    position_difference = 0 # różnica między pozycją według AI a rzeczywistą pozycją
    rotation_difference = 0 # różnica między rotacją obiektu według AI a rzeczywistą rotacją

    while run:
        #print(clock.get_rawtime())
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if (lines + 1) % 10 == 0:
            lines = 0
            level += 1
            if fall_speed > 0.12:
                fall_speed -= 0.05

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        if(net == None):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_piece.x -= 1
                        if not (valid_space(current_piece, grid)):
                            current_piece.x += 1
                    if event.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not (valid_space(current_piece, grid)):
                            current_piece.x -= 1
                    if event.key == pygame.K_DOWN:
                        while valid_space(current_piece, grid):
                            current_piece.y += 1
                        current_piece.y -=1
                    if event.key == pygame.K_UP:
                        current_piece.rotation += 1
                        if not (valid_space(current_piece, grid)):
                            current_piece.rotation -= 1
        else:
            if (use_nn):
                predict_position, predict_rotation = get_output(net,grid, current_piece, next_piece)
                position_difference = predict_position - current_piece.x

                if predict_rotation == 4:
                    predict_rotation -= 1
                rotation_difference = abs(predict_rotation - current_piece.rotation % 4)
                use_nn = False
                #print(predict_position, predict_rotation)

            #prin(output[0], output[1])

            # obracamy tetrimino
            if rotation_difference != 0:
                current_piece.rotation += 1
                rotation_difference -= 1
                if not (valid_space(current_piece, grid)):
                    current_piece.rotation -= 1
                    rotation_difference =0

            #przesuwamy tetrimino
            if abs(position_difference) != 0:
                delta = int(1 * numpy.sign(position_difference))
                current_piece.x += delta
                position_difference -= delta
                if not (valid_space(current_piece, grid)):
                    current_piece.x -= delta
                    position_difference += delta
                    position_difference = 0
            #print(position_difference, current_piece.x)

            if abs(position_difference) == 0 and rotation_difference == 0:
                while valid_space(current_piece, grid):
                    current_piece.y += 1
                current_piece.y -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            use_nn = True
            change_piece = False
            cleared_lines = clear_rows(grid, locked_positions)
            score += calculate_score(cleared_lines, level)
            lines += cleared_lines
            #print(score)
        if(win != None):
            draw_window(win, grid, score)
            draw_next_shape(next_piece, win)
            pygame.display.update()

        # przeliczanie nowego dopasowania
        if(genome != None):
            genome.fitness = calculate_fitness(score, level, lines, locked_positions)

        if check_lost(locked_positions):
            if(win != None):
                draw_text_middle(win, "YOU LOST!", 80, (255, 255, 255))
                pygame.display.update()
            #pygame.time.delay(1500)
            if(genome != None):
                genome.fitness -= 20
            run = False

        if genome != None and (score > 5000 or level * 10 + lines > 50):
            run = False
        #print(shapes.index(current_piece.shape), current_piece.x,current_piece.y, current_piece.rotation)
    #print(score, genome.fitness)



#ustawienie pliku konfiguracyjnego
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config-feedforward')

# stworzenie populacji początkowej
p = neat.Population(config)
p.add_reporter(neat.StdOutReporter(False))

# ustawienie równoległego obliczania ??
# neat.parallel.ParallelEvaluator(4,evaluate_genome)

# wykonanie ewolucji
winner = p.run(evaluate_genome, 50)

#win = pygame.display.set_mode((s_width, s_height))
#pygame.display.set_caption('Tetris')
#main(win)

# orzymanie "najlepszego" osobnika
winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

with open("winner.pkl", "wb") as f:
    pickle.dump(winner, f)
    f.close()

while(True):
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('Tetris')
    main(win, winner_net)
    pygame.display.quit()

