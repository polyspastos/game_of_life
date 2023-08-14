import pygame
import numpy as np
import time
import os
import tkinter as tk
from tkinter import filedialog

cell_size = 10
initial_board_size = 55
board = np.zeros((initial_board_size, initial_board_size), dtype=int)
pause_flag = True
generation_interval = 100

pygame.init()
window_size = (
    initial_board_size * cell_size + 400,
    initial_board_size * cell_size + 400,
)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("cellular automaton simulator")

clock = pygame.time.Clock()


def draw_instructions():
    rows, cols = board.shape
    grid_width = cols * cell_size
    grid_height = rows * cell_size
    # font = pygame.font.SysFont(None, 32)
    font = pygame.font.SysFont("verdana", 24)

    instruction_text = [
        "SPACE - start/pause",
        "S - save",
        "R - random seed",
        "L - load",
    ]
    for line in instruction_text:
        instruction_surface = font.render(line, True, (0, 0, 0))
        window.blit(
            instruction_surface,
            (grid_width + 50, grid_height + 50 + 50 * instruction_text.index(line)),
        )
    # print(pygame.font.get_fonts())
    pygame.display.update(
        (grid_width, grid_height, grid_width + 450, grid_height + 450)
    )
    pygame.display.update(
        (grid_width, grid_height, grid_width + 450, grid_height + 450)
    )


def generate_glider_gun():
    global board
    board[5][1] = board[5][2] = 1
    board[6][1] = board[6][2] = 1
    board[3][13] = board[3][14] = 1
    board[4][12] = board[4][16] = 1
    board[5][11] = board[5][17] = 1
    board[6][11] = board[6][15] = board[6][17] = board[6][18] = 1
    board[7][11] = board[7][17] = 1
    board[8][12] = board[8][16] = 1
    board[9][13] = board[9][14] = 1
    board[1][25] = 1
    board[2][23] = board[2][25] = 1
    board[3][21] = board[3][22] = 1
    board[4][21] = board[4][22] = 1
    board[5][21] = board[5][22] = 1
    board[6][23] = board[6][25] = 1
    board[7][25] = 1


def update_grid():
    global board, pause_flag
    if not pause_flag:
        new_board = np.copy(board)
        rows, cols = board.shape
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                neighbors = (
                    board[i - 1][j - 1]
                    + board[i - 1][j]
                    + board[i - 1][j + 1]
                    + board[i][j - 1]
                    + board[i][j + 1]
                    + board[i + 1][j - 1]
                    + board[i + 1][j]
                    + board[i + 1][j + 1]
                )

                if board[i][j] == 1:
                    if neighbors < 2 or neighbors > 3:
                        new_board[i][j] = 0
                else:
                    if neighbors == 3:
                        new_board[i][j] = 1

        board = new_board


def toggle_pause():
    global pause_flag
    pause_flag = not pause_flag


def draw_grid():
    window.fill((255, 255, 255))

    rows, cols = board.shape
    grid_width = cols * cell_size
    grid_height = rows * cell_size

    for i in range(rows):
        for j in range(cols):
            if board[i][j] == 1:
                pygame.draw.rect(
                    window,
                    (0, 0, 0),
                    (j * cell_size, i * cell_size, cell_size - 1, cell_size - 1),
                )

    pygame.display.update((0, 0, grid_width, grid_height))


def save_generation():
    global board
    timestamp = str(int(time.time()))
    file_name = f"generation_{timestamp}.txt"
    invalid_chars = r'\/:*?"<>|'
    for char in invalid_chars:
        file_name = file_name.replace(char, "_")

    with open(file_name, "w") as f:
        for row in board:
            line = "".join(map(str, row))
            f.write(line + "\n")


def load_generation(file_path):
    global board
    with open(file_path, "r") as f:
        lines = f.readlines()
        board = np.array([list(map(int, line.strip())) for line in lines])

    draw_grid()


def generate_random_seed():
    global board
    board = np.random.randint(2, size=(initial_board_size, initial_board_size))
    draw_grid()


def load_game_state():
    global board
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="select a gamestate file",
        filetypes=[("text files", "*.txt"), ("all files", "*.*")],
    )

    if file_path:
        load_generation(file_path)


initial_file_path = "initial_generation.txt"
if os.path.exists(initial_file_path):
    load_generation(initial_file_path)
else:
    generate_glider_gun()

running = True
generation_timer = pygame.USEREVENT + 1
pygame.time.set_timer(generation_timer, generation_interval)

draw_instructions()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                toggle_pause()
            elif event.key == pygame.K_s:
                save_generation()
            elif event.key == pygame.K_r:
                generate_random_seed()
            elif event.key == pygame.K_l:
                load_game_state()
        elif event.type == generation_timer:
            update_grid()

    draw_grid()
    draw_instructions()
    # pygame.display.update()
    clock.tick(60)

pygame.quit()
