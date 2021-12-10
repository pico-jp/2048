from copy import deepcopy
import itertools
from math import fabs
from random import randint, random

class game2048():

    def __init__(self, size_board):
        self.size_board = size_board
        self.verbose = False
        self.observation_1d = False
        self.goal = 2048

    def reset(self):
        self.setup_board()
        self.score = 0
        self.num_step = 0
        self.done = False
        if self.verbose: self.print_board()
        return self.board

    def print_board(self):
        max_str_len = 0
        for row in self.board:
            temp = len(str(max(row)))
            max_str_len = temp if temp > max_str_len else max_str_len
        print('-' * ((max_str_len + 3) * self.size_board + 1))
        for row in self.board:
            temp = deepcopy(row)
            temp = list(map(lambda x: str(x).rjust(max_str_len), temp))
            temp = f'| {" | ".join(temp)} |'
            print(temp)
            print('-' * ((max_str_len + 3) * self.size_board + 1))
        return self.board

    def setup_board(self):
        self.board = [[0] * self.size_board for i in range(self.size_board)]
        self.add_number()
        self.add_number()

    def add_number(self):
        options = []
        for i in range(self.size_board):
            for j in range(self.size_board):
                if self.board[i][j] == 0: options.append([i, j])
        if len(options) > 0:
            spot = randint(0, len(options) - 1)
            i = options[spot][0]
            j = options[spot][1]
            r = random()
            self.board[i][j] = 2 if r < 0.9 else 4

    def slide(self, row):
        array = list(filter(lambda x: x > 0, row))
        missing = self.size_board - len(array)
        array = [0] * missing + array
        return array

    def combine(self, row):
        for j in reversed(range(1, self.size_board)):
            a = row[j]
            b = row[j - 1]
            if a == b:
                row[j] = a + b
                row[j - 1] = 0
                self.score += row[j]
                self.score_inc = row[j]
        return row

    def operate(self, row):
        row = self.slide(row)
        row = self.combine(row)
        row = self.slide(row)
        return row

    def flip(self):
        for i in range(self.size_board):
            self.board[i] = self.board[i][::-1]

    def transpose(self):
        self.board = [list(x) for x in zip(*self.board)]

    def is_game_over(self):
        for i in range(self.size_board):
            if 0 in self.board[i]: return False
            for j in range(self.size_board):
                if i != self.size_board - 1 and self.board[i][j] == self.board[i + 1][j]: return False
                if j != self.size_board - 1 and self.board[i][j] == self.board[i][j + 1]: return False
        return True

    def is_game_won(self):
        for row in self.board:
            if self.goal in row: return True
        return False

    class action_space():
        def sample():
            return randint(0, 3)

    def step(self, action):
        board_past = deepcopy(self.board)
        flipped = False
        transposed = False
        played = True
        self.score_inc = 0
        self.num_step += 1

        if action == 0:
            key = 'R'
        elif action == 1:
            key = 'L'
            self.flip()
            flipped = True
        elif action == 2:
            key = 'D'
            self.transpose()
            transposed = True
        elif action == 3:
            key = 'U'
            self.transpose()
            self.flip()
            transposed = True
            flipped = True
        else:
            played = False

        if played:
            for i in range(self.size_board):
                self.board[i] = self.operate(self.board[i])
            if self.verbose: print(f'step = {self.num_step}, key = {key}, score_inc = {self.score_inc}, score = {self.score}')

            if flipped:
                self.flip()

            if transposed:
                self.transpose()

            if self.board != board_past:
                self.add_number()

            if self.verbose: self.print_board()

            if self.is_game_over():
                if self.verbose: print(f'GAME OVER, score = {self.score}')
                self.done =  True

            if self.is_game_won():
                if self.verbose: print(f'GAME WON, score = {self.score}')
                self.done = True

        if self.observation_1d: return list(itertools.chain.from_iterable(self.board)), self.score_inc, self.done, self.num_step
        return self.board, self.score_inc, self.done, self.score

    def config(self, goal=2048, observation_1d=True, verbose=False):
        self.goal = goal
        self.observation_1d = observation_1d
        self.verbose = verbose

    def close(self):
        pass

if __name__ == '__main__':
    env = game2048(size_board=4)
    env.config(goal=2048, observation_1d=False, verbose=False)
    for i_episode in range(20):
        observation = env.reset()
        for t in range(10000):
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)
            if done:
                print(f'Episode finished after {t + 1} steps (max_tile: {max(list(itertools.chain.from_iterable(observation)))}, score: {info})')
                break


