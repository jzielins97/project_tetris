import tetris


def main(win, net = None):  # *
    locked_positions = {}
    grid = tetris.create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = tetris.get_shape()
    next_piece = tetris.get_shape()
    clock = tetris.pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.36 #0.27
    score = 0
    lines = 0
    level = 0

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

            if event.type == tetris.pygame.KEYDOWN:
                if event.key == tetris.pygame.K_LEFT:
                    current_piece.x -= 1
                    if not (tetris.valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == tetris.pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (tetris.valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == tetris.pygame.K_DOWN:
                    while tetris.valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -=1
                if event.key == tetris.pygame.K_UP:
                    current_piece.rotation += 1
                    if not (tetris.valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

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
main(win)
