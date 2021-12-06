import numpy as np
from random import randint, random
from copy import deepcopy
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
    size_board = len(row)
    for j in reversed(range(1, size_board)):
        a = row[j]
        b = row[j - 1]
        if a == b:
            row[j] = a + b
            row[j - 1] = 0
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
            pygame.draw.rect(screen, color_grid, Rect(pos_x, pos_y, pos_x + size_tile, pos_y + size_tile), 2)
            tile = board[i][j]
            if tile != 0:
                font = pygame.font.SysFont(None, size_tile // 2)
                text = font.render(str(tile), True, color_num)
                text_rect = text.get_rect(center=(pos_x + size_tile * 0.5, pos_y + size_tile * 0.5))
                screen.blit(text, text_rect)

def key_pressed(board):
    size_board = len(board)
    for i in range(size_board):
        board[i] = operate(board[i])
    board = add_number(board)    
    return board

size_board = 4
color_board = (255, 255, 255)
color_tile = (150, 150, 150)
color_num = (0, 0, 255)
color_grid = (0, 0, 0)
size_tile = 100

print('slide', slide([0, 2, 0, 2]))
print('combine', combine([2, 2, 2, 2]))
print('combine', combine([2, 4, 2, 2]))

print('operate', operate([2, 2, 2, 2]))  # 0044
print('operate', operate([2, 4, 2, 2]))  # 0244
print('operate', operate([0, 2, 2, 4]))  # 0044

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
            if event.key == pygame.K_SPACE:
                board = key_pressed(board)

    draw(board, size_tile)
    pygame.display.update()

    