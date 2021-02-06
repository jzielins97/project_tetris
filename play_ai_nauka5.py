import tetris
import numpy
import pickle
import neat


def get_input(grid, current_piece, next_piece):
    _input = []
    height = [20] * 10 # maksymalna wyokość kolumny
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if i > height[j]:
                _input.append(1)
                continue

            if grid[i][j] == (0, 0, 0,):
                _input.append(0)
            else:
                _input.append(1)
                height[j] = i

    for i in range(len(tetris.shapes)):
        if i == tetris.shapes.index(current_piece.shape):
            _input.append(1)
        else:
            _input.append(0)

    for i in range(len(tetris.shapes)):
        if i == tetris.shapes.index(next_piece.shape):
            _input.append(1)
        else:
            _input.append(0)

    return _input


def get_output(net, grid, current_piece, next_piece):
    _input = get_input(grid, current_piece, next_piece)
    _output = net.activate(_input)
    """
    # wersja dla 2 wejść, gdzie pierwsza wartość oznacza kolumnę (0.0-1.0 -> 0-9)
    #                          druga wartość oznacza rotację (0.0-1.0 -> 0-3)
    rotation = int(_output[1] * 4)
    if rotation == 4:
        rotation -= 1
    position = int(_output[0] * 10)

    return position, rotation
    """
    # wersja dla 40 wyjść, gdzie każdy output oznacza inną kombinację kolumny i rotacji dla danego tetrimino
    best_index = _output.index(max(_output))

    return best_index % 10, best_index // 10


def main(win, net = None):  # *
    locked_positions = {}
    grid = tetris.create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = tetris.get_shape()
    next_piece = tetris.get_shape()
    clock = tetris.pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.12 #0.27
    score = 0
    lines = 0
    level = 0
    use_nn = True

    while run:
        grid = tetris.create_grid(locked_positions)
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
            if not (tetris.valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in tetris.pygame.event.get():
            if event.type == tetris.pygame.QUIT:
                run = False
                tetris.pygame.display.quit()

        if (use_nn):
            predict_position, predict_rotation = get_output(net, grid, current_piece, next_piece)
            position_difference = predict_position - current_piece.x
            rotation_difference = abs(predict_rotation - current_piece.rotation % 4)
            #print(predict_position, predict_rotation)
            use_nn = False


        # obracamy tetrimino
        if rotation_difference != 0:
            current_piece.rotation += 1
            rotation_difference -= 1
            if not (tetris.valid_space(current_piece, grid)):
                current_piece.rotation -= 1
                rotation_difference = 0

        # przesuwamy tetrimino
        if abs(position_difference) != 0:
            delta = int(1 * numpy.sign(position_difference))
            current_piece.x += delta
            position_difference -= delta
            if not (tetris.valid_space(current_piece, grid)):
                current_piece.x -= delta
                position_difference += delta
                position_difference = 0
        # print(position_difference, current_piece.x)

        """
        # zrzucenie klocka na pozycje
        if abs(position_difference) == 0 and rotation_difference == 0:
            while tetris.valid_space(current_piece, grid):
                current_piece.y += 1
            current_piece.y -= 1
        """
        shape_pos = tetris.convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            #print(locked_positions)
            current_piece = next_piece
            next_piece = tetris.get_shape()
            change_piece = False
            use_nn = True
            cleared_lines = tetris.clear_rows(grid, locked_positions)
            score += tetris.calculate_score(cleared_lines, level)
            lines += cleared_lines

        tetris.draw_window(win, grid, score)
        tetris.draw_next_shape(next_piece, win)
        tetris.pygame.display.update()

        if tetris.check_lost(locked_positions):
            tetris.draw_text_middle(win, "YOU LOST!", 80, (255, 255, 255))
            tetris.pygame.display.update()
            tetris.pygame.time.delay(1500)
            run = False


win = tetris.pygame.display.set_mode((tetris.s_width, tetris.s_height))
tetris.pygame.display.set_caption('Tetris')

# ustawienie pliku konfiguracyjnego
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     '.\\configs\\config-5')

with open(".\\results\\winner_nauka_5_1000.pkl", "rb") as f:
    winner = pickle.load(f)

net = neat.nn.FeedForwardNetwork.create(winner, config)

main(win, net)
