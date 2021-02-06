# https://www.askforgametask.com/tutorial/machine-learning/ai-plays-tetris-with-cnn/
# https://www.techwithtim.net/tutorials/game-development-with-python/tetris-pygame/tutorial-1/
# https://www.youtube.com/watch?v=wQWWzBHUJWM&ab_channel=TechWithTim

import neat
import numpy
import pickle
import tetris as tr


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

    for i in range(len(tr.shapes)):
        if i == tr.shapes.index(current_piece.shape):
            _input.append(1)
        else:
            _input.append(0)

    for i in range(len(tr.shapes)):
        if i == tr.shapes.index(next_piece.shape):
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


# obliczanie dopasowania
def calculate_fitness(score, level, lines, locked):
    if score > 0:
        fitness = score / (level * 10 + lines)
    else:
        fitness = 0


    height = [0] * 10 # wysokości poszczególnych kolumn
    max_y = 20 # wysokość najwyższego klocka
    # sprawdzenie jak wysoka jest nasza powierzchnia:
    for y in range(20): # skanowanie od góry do dołu
        line = 0
        for x in range(10):  # skanowanie od lewej do prawej
            if (x,y) in locked:
                if y < max_y: # sprawdzamy wysokość
                    max_y = y

                if 20 - y > height[x]:
                    height[x] = 20 - y
                if (x,y+1) not in locked and y+1 < 20: # sprawdzamy czy są dziury w ostatecznej strukturze (dziura to klocek pod, którym jest pusto)
                    fitness -= 50

    dh = 0
    for i, h in enumerate(height):
        try:
            dh += abs(h - height[i+1])
        except:
            continue

    fitness -= dh
    fitness -= 5 * (20 - max_y) # kara za wysokość stworzonej struktury

    return fitness


def evaluate_genome(genomes, config):  #
    # losowanie 10 zestawów tetrimino (po 20) do testowania osobników:
    pieces_sets = []
    for i in range(20):
        pieces_sets.append(numpy.random.randint(0, 6, 20))

    for genome_id, genome in genomes: # pętla po wszystkich osobnikach
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        fitness_avg = 0
        lost_count = 0
        for set_i in pieces_sets:
            win = None #tr.pygame.display.set_mode((tr.s_width, tr.s_height))
            #tr.pygame.display.set_caption('Tetris')

            """ ustawienia gry. """
            clock = tr.pygame.time.Clock()
            fall_time = 0
            fall_speed = 0.02  # 0.02

            """ Każdy osobnik musi mieć informację o tetrimino, które kontroluje i następnym tetrimino
                Musi też mieć informacje o gridzie jaki teraz ma."""
            locked_positions = {}

            current_piece = tr.get_shape_i(set_i[0])
            next_piece = tr.get_shape_i(set_i[1])
            next_index = 2

            change_piece = False # czy nastąpiło zatrzymanie klocka
            run = True # czy gra toczy się dalej

            score = 0  # zdobyte punkty
            lines = 0  # ile linii zostało wyczyszczonych
            level = 0  # osiągnięty poziom gry
            use_nn = True # czy wykonać predykcji dla tetrimino?

            position_difference = 0  # różnica między pozycją według AI a rzeczywistą pozycją
            rotation_difference = 0  # różnica między rotacją obiektu według AI a rzeczywistą rotacją

            while run and next_index < len(set_i):
                grid = tr.create_grid(locked_positions)
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
                    if not (tr.valid_space(current_piece, grid)) and current_piece.y > 0:
                        current_piece.y -= 1
                        change_piece = True


                if (use_nn):
                    predict_position, predict_rotation = get_output(net, grid, current_piece, next_piece)
                    position_difference = predict_position - current_piece.x
                    rotation_difference = abs(predict_rotation - current_piece.rotation % 4)

                    use_nn = False

                # obracamy tetrimino
                if rotation_difference != 0:
                    current_piece.rotation += 1
                    rotation_difference -= 1
                    if not (tr.valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                        rotation_difference = 0

                # przesuwamy tetrimino
                if abs(position_difference) != 0:
                    delta = int(1 * numpy.sign(position_difference))
                    current_piece.x += delta
                    position_difference -= delta
                    if not (tr.valid_space(current_piece, grid)):
                        current_piece.x -= delta
                        position_difference += delta
                        position_difference = 0
                # print(position_difference, current_piece.x)

                #zrzucenie klocka na pozycje
                if abs(position_difference) == 0 and rotation_difference == 0:
                    while tr.valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1

                shape_pos = tr.convert_shape_format(current_piece)

                for i in range(len(shape_pos)):
                    x, y = shape_pos[i]
                    if y > -1:
                        grid[y][x] = current_piece.color

                if change_piece:
                    for pos in shape_pos:
                        p = (pos[0], pos[1])
                        locked_positions[p] = current_piece.color
                    current_piece = next_piece
                    next_piece = tr.get_shape_i(set_i[next_index])
                    next_index += 1
                    use_nn = True
                    change_piece = False
                    cleared_lines = tr.clear_rows(grid, locked_positions)
                    score += tr.calculate_score(cleared_lines, level)
                    lines += cleared_lines
                if (win != None):
                    tr.draw_window(win, grid, score)
                    tr.draw_next_shape(next_piece, win)
                    tr.pygame.display.update()

                if tr.check_lost(locked_positions):
                    if (win != None):
                        tr.draw_text_middle(win, "YOU LOST!", 80, (255, 255, 255))
                        tr.pygame.display.update()
                    lost_count += len(set_i) - next_index # za każdy niewykorzystany tetrimino
                    run = False

            fitness_avg = calculate_fitness(score, level, lines, locked_positions)
            tr.pygame.display.quit()
        fitness_avg -= lost_count * 100
        genome.fitness = fitness_avg / len(pieces_sets)
        #print("lost",lost_count)


# ustawienie pliku konfiguracyjnego
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config-feedforward')

try:
    p = neat.checkpoint.Checkpointer.restore_checkpoint(".\\checkpoints\\nauka_5\\neat-checkpoint-699")
except IOError:
    # stworzenie populacji początkowej
    print("File does not exist")
    p = neat.Population(config)

try:
    with open(".\\checkpoints\\nauka_5\\stats.pkl", "rb") as f:
        stats = pickle.load(f)
except:
    print("No presaved stats")
    stats = neat.StatisticsReporter()

p.add_reporter(neat.StdOutReporter(False))
p.add_reporter(stats)
p.add_reporter(neat.Checkpointer(generation_interval=5, filename_prefix=".\\checkpoints\\nauka_5\\neat-checkpoint-")) # zapisywanie progresu populacji co 5 generacja


# wykonanie ewolucji
winner = p.run(evaluate_genome, 302)

#zapisywanie statystyk:
with open(".\\checkpoints\\nauka_5\\stats.pkl", "wb") as f:
    pickle.dump(stats, f)
    f.close()


# otrzymanie "najlepszego" osobnika
winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
with open("winner.pkl", "wb") as f:
    pickle.dump(winner, f)
    f.close()
