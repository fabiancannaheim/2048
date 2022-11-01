
# Author:      Fabian C. Annaheim
# Date:        01.11.2022
# Copyright:   https://github.com/fabiancannaheim/2048
# Description: This script contains an implementation of expectimax algorithm
#              which traverses a game tree depth-first and scores moves via
#              several heuristic functions as well as probabilistic properties
#              which are determined by the game itself (for 2048 the tile spawns)

import random
import game
import sys
import numpy as np

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

EXPECTIMAX_START_DEPTH = 0

HEURISTIC_WEIGHT_CORNERS = 1
HEURISTIC_WEIGHT_NEIGHBOURS = 1
HEURISTIC_WEIGHT_MONOTICITY = 1
HEURISTIC_WEIGHT_EMPTY_FIELDS = 1

HEURISTIC_CORNERS_MIN, HEURISTIC_CORNERS_MAX = 0, 6
HEURISTIC_EMPTY_FIELDS_MIN, HEURISTIC_EMPTY_FIELDS_MAX = 0, 14
HEURISTIC_MONOTICITY_MIN, HEURISTIC_MONOTICITY_MAX = 0, 8
HEURISTIC_NEIGHBOURS_MIN, HEURISTIC_NEIGHBOURS_MAX = 0, 20

def find_best_move(board):
    result = [score_toplevel_move(i, board, max_depth(board)) for i in [UP, DOWN, LEFT, RIGHT]]
    bestmove = result.index(max(result))
    for m in [UP, DOWN, LEFT, RIGHT]:
        print("move: %d score: %.4f" % (m, result[m]))
    return bestmove


def score_toplevel_move(move, board, max_depth):
    newboard = execute_move(move, board)
    if board_equals(board, newboard):
        return 0
    else:
        return expectimax(newboard, EXPECTIMAX_START_DEPTH, max_depth, probabilistic=True)


def expectimax(board, depth, max_depth, probabilistic):
    if depth == max_depth:
        return board_score(board)
    elif probabilistic:
        score = 0
        empty_fields = get_empty_fields(board)
        len_empty_fields = len(empty_fields)
        for i in range(len_empty_fields):
            board_2_spawn = emit_tile(board.copy(), 2, empty_fields[i][0], empty_fields[i][1])
            board_4_spawn = emit_tile(board.copy(), 4, empty_fields[i][0], empty_fields[i][1])
            score += 0.9 * expectimax(board_2_spawn, depth + 1, max_depth, probabilistic=False)
            score += 0.1 * expectimax(board_4_spawn, depth + 1, max_depth, probabilistic=False)
        return score / len_empty_fields
    else:
        best_score = 0
        for i in [UP, DOWN, LEFT, RIGHT]:
            new_board = execute_move(i, board)
            if board_equals(board, new_board):
                continue
            else:
                score = expectimax(new_board, depth + 1, max_depth, probabilistic=True)
                if score > best_score:
                    best_score = score
        return best_score


# Score for a particular board

def board_score(board):

    corners = check_corners(board)
    empty_fields = count_empty_fields(board)
    neighbours = count_neighbours(board)
    monoticity = compute_monoticity(board)

    return (
            HEURISTIC_WEIGHT_CORNERS * corners
            + HEURISTIC_WEIGHT_EMPTY_FIELDS * empty_fields
            + HEURISTIC_WEIGHT_NEIGHBOURS * neighbours
            + HEURISTIC_WEIGHT_MONOTICITY * monoticity
    )


# Heuristics

def count_empty_fields(board):
    zeros = 0
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j] == 0:
                zeros = zeros + 1
    return (zeros - HEURISTIC_EMPTY_FIELDS_MIN) / (HEURISTIC_EMPTY_FIELDS_MAX - HEURISTIC_EMPTY_FIELDS_MIN)


def check_corners(board):

    sorted_board = np.sort(np.array(board).ravel())[::-1]

    max_value = sorted_board[0]
    podium_values = [sorted_board[1], sorted_board[2]]

    areas = {
        'ul': {'corner': board[0][0], 'neighbours': [board[1][0], board[0][1]]},
        'ur': {'corner': board[0][3], 'neighbours': [board[0][2], board[1][3]]},
        'll': {'corner': board[3][0], 'neighbours': [board[3][1], board[2][0]]},
        'lr': {'corner': board[3][3], 'neighbours': [board[3][2], board[2][3]]}
    }

    score = 0

    for i in areas:
        if areas[i]['corner'] == max_value:
            if all(item in areas[i]['neighbours'] for item in podium_values):
                score = 12
            elif any(item in areas[i]['neighbours'] for item in podium_values):
                score = 6
            else:
                score = 3
            break

    return (score - HEURISTIC_CORNERS_MIN) / (HEURISTIC_CORNERS_MAX - HEURISTIC_CORNERS_MIN)


def count_neighbours(board):
    neighbours = 0
    transposed = board.T
    for i in range(0, len(board)):
        last = [False, False]
        for j in range(0, len(board[i])):
            if board[i][j] != 0 and last[0] and last[0] == board[i][j]:
                neighbours = neighbours + 1
            if transposed[i][j] != 0 and last[1] and last[1] == transposed[i][j]:
                neighbours = neighbours + 1
            last[0] = board[i][j]
            last[1] = transposed[i][j]
    return (neighbours - HEURISTIC_NEIGHBOURS_MIN) / (HEURISTIC_NEIGHBOURS_MAX - HEURISTIC_NEIGHBOURS_MIN)


def compute_monoticity(board):
    transposed = board.T
    score = 0
    for i in range(0, len(board)):
        if monotonic(board[i]) and not np.all(board[i] == 0):
            score += 1
        if monotonic(transposed[i]) and not np.all(transposed[i] == 0):
            score += 1
    return (score - HEURISTIC_MONOTICITY_MIN) / (HEURISTIC_MONOTICITY_MAX - HEURISTIC_MONOTICITY_MIN)


# Helpers

def execute_move(move, board):
    if move == UP:
        return game.merge_up(board)
    elif move == DOWN:
        return game.merge_down(board)
    elif move == LEFT:
        return game.merge_left(board)
    elif move == RIGHT:
        return game.merge_right(board)
    else:
        sys.exit("No valid move")


def monotonic(x):
    dx = np.diff(x)
    return np.all(dx <= 0) or np.all(dx >= 0)

def emit_tile(board, val, x, y):
    board[x][y] = val
    return board


def find_best_move_random_agent():
    return random.choice([UP, DOWN, LEFT, RIGHT])


def board_equals(board, newboard):
    return (newboard == board).all()


def normalize(data):
    xmin = min(data)
    xmax = max(data)
    if xmax - xmin == 0:
        return data
    for i in range(0, len(data)):
        data[i] = (data[i] - xmin) / (xmax - xmin)
    return data


def max_depth(board):
    number_empty_fields = count_empty_fields(board)
    if number_empty_fields > 6:
        max_depth = 2
    elif number_empty_fields > 2:
        max_depth = 3
    else:
        max_depth = 4
    return max_depth


def get_empty_fields(board):
    fields = []
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j] == 0:
                fields.append([i, j])
    return fields
