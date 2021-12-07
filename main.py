from copy import deepcopy
from random import randint, random
import numpy as np
import pygame
from pygame.locals import *

def print_as_np_array(A):
    print(np.array(A))

def setup(size_board):
    board = [[0] * size_board for i in range(size_board)]
    add_number(board)
    add_number(board)
    return board

def add_number(board):
    size_board = len(board)
    options = []
    for i in range(size_board):
        for j in range(size_board):
            if board[i][j] == 0: options.append([i, j])
    if len(options) > 0:
        spot = randint(0, len(options) - 1)
        i = options[spot][0]
        j = options[spot][1]
        r = random()
        board[i][j] = 2 if r < 0.9 else 4
    return board

def slide(row):
    size_board = len(row)
    array = list(filter(lambda x: x > 0, row))
    missing = size_board - len(array)
    array = [0] * missing + array
    return array

def combine(row):
    global score
    size_board = len(row)
    for j in reversed(range(1, size_board)):
        a = row[j]
        b = row[j - 1]
        if a == b:
            row[j] = a + b
            row[j - 1] = 0
            score += row[j]
    return row

def operate(row):
    row = slide(row)
    row = combine(row)
    row = slide(row)
    return row

def draw(board, size_tile):
    size_board = len(board)
    for i in range(size_board):
        for j in range(size_board):
            pos_x = j * size_tile
            pos_y = i * size_tile
            pygame.draw.rect(screen, color_grid, Rect(pos_x, pos_y, pos_x + size_tile, pos_y + size_tile), 10)
            tile = board[i][j]
            if tile != 0:
                font = pygame.font.SysFont(None, size_tile // 2)
                text = font.render(str(tile), True, color_num)
                text_rect = text.get_rect(center=(pos_x + size_tile * 0.5, pos_y + size_tile * 0.5))
                screen.blit(text, text_rect)

def flip(board):
    size_board = len(board)
    for i in range(size_board):
        board[i] = board[i][::-1]
    return board

def transpose(board):
    board = [list(x) for x in zip(*board)]
    return board

def is_game_over(board):
    size_board = len(board)
    for i in range(size_board):
        if 0 in board[i]: return False
        for j in range(size_board):
            if i != size_board - 1 and board[i][j] == board[i + 1][j]: return False
            if j != size_board - 1 and board[i][j] == board[i][j + 1]: return False
    return True

def key_pressed(board):
    size_board = len(board)
    board_past = deepcopy(board)
    flipped = False
    transposed = False
    played = True

    if event.key == pygame.K_RIGHT:
        key = 'R'
        pass
    elif event.key == pygame.K_LEFT:
        key = 'L'
        board = flip(board)
        flipped = True
    elif event.key == pygame.K_DOWN:
        key = 'D'
        board = transpose(board)
        transposed = True
    elif event.key == pygame.K_UP:
        key = 'U'
        board = transpose(board)
        board = flip(board)
        transposed = True
        flipped = True
        pass
    else:
        played = False

    if played:
        for i in range(size_board):
            board[i] = operate(board[i])
        print(f'key = {key}, score = {score}')

        if flipped:
            board = flip(board)

        if transposed:
            board = transpose(board)

        if board != board_past:
            board = add_number(board)
            print_as_np_array(board)

        if is_game_over(board):
            print('GAME OVER')
            exit()

    return board

size_board = 4
color_board = (205, 191, 180)
color_tile = (150, 150, 150)
color_num = (118, 110, 101)
color_grid = (188, 172, 159)
size_tile = 100
score = 0

board = setup(size_board = size_board)
print_as_np_array(board)


# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption('2048')

# Game loop
running = True
while running:
    screen.fill(color_board)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            board = key_pressed(board)

    draw(board, size_tile)
    pygame.display.update()

    