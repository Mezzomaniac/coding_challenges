from downloader import download
import numpy as np

download(2021, 4)
with open('aoc2021_4input.txt') as inputfile:
    input = inputfile.read()
print(input)
boards = input.split('\n\n')
draws = [int(n) for n in boards[0].split(',')]
original_boards = np.array([[[int(n) for n in row.split()] for row in board.splitlines()] for board in boards[1:]], dtype=float)
print(draws)
print(original_boards)

def winner(boards):
    for axis in (1, 2):
        try:
            return np.nonzero(np.all(np.isnan(boards), axis=axis))[0][0]
        except IndexError:
            pass

boards = original_boards.copy()
for draw in draws:
    boards[boards == draw] = np.nan
    winner_index = winner(boards)
    if winner_index is not None:
        score = draw * np.nansum(boards[winner_index])
        break
print(int(score))


def loser(boards):
    winners = set()
    for axis in (1, 2):
        winners |= set(np.nonzero(np.all(np.isnan(boards), axis=axis))[0])
    losers = set(range(len(boards))) - winners
    if len(losers) == 1:
        return losers.pop()
    elif not losers:
        raise ValueError

boards = original_boards.copy()
loser_index = None
for draw in draws:
    boards[boards == draw] = np.nan
    try:
        loser_index = loser(boards)
    except ValueError:
        score = draw * np.nansum(boards[loser_index])
        break
print(int(score))
