# setting up the import form the ../utils folder
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir + "/utils")

from print_util import print_9x9_board
from grid_transforms import flatten_grid

from random import sample

def pattern(i, j, SQ_GRID = 3, GRID_SIZE = 9):
    """
    This function makes sure that the elements do not repeat.
    """
    return (SQ_GRID * (i%SQ_GRID) + i//SQ_GRID + j) % GRID_SIZE

def shuffle(s):
    '''
    Shuffle a list of numbers
    '''
    return sample(s, len(s))

def generate_unsolved_sudoku(number_of_zeros, SQ_GRID = 3, GRID_SIZE = 9):
    rBase = range(SQ_GRID)

    # generating a row of elements
    row = []
    for i in shuffle(rBase):
        for j in shuffle(rBase):
            row.append(j*SQ_GRID + i)

    # generating a column of elements
    column = []
    for i in shuffle(rBase):
        for j in shuffle(rBase):
            column.append(j * SQ_GRID + i)

    # nums are the elements that are present in the Sudoku
    nums = shuffle(range(1, GRID_SIZE + 1))

    # generating every element in the grid (total number of elements = grid_size^2)
    grid = [ [nums[pattern(i, j, SQ_GRID, GRID_SIZE)] for j in column] for i in row ]

    # deleting elements randomly (setting them to 0)
    number_of_elements = GRID_SIZE ** 2
    for p in sample(range(number_of_elements), number_of_zeros):
        grid[p//GRID_SIZE][p%GRID_SIZE] = 0

    return grid

## TESTING

# SQ_GRID = 3
# GRID_SIZE = SQ_GRID ** 2
# number_of_zeros = 20
#
# unsolved_grid = generate_unsolved_sudoku(number_of_zeros, SQ_GRID, GRID_SIZE)
#
# print("\nBoard after random element deletion (number of zeros = " + str(number_of_zeros) + "):")
# for line in unsolved_grid:
#     print(line)
#
# flat_unsolved_grid = flatten_grid(unsolved_grid)
# print("\nThe grid as a flat list:\n" + str(flat_unsolved_grid))
#
# print("\nPretty printed grid:")
# print_9x9_board(unsolved_grid)

# TODO: add docstring