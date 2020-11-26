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

def flatten_grid(grid):
    """
    Flattens a grid that represents a Sudoku board.

    Input: A list of lists. The sub-lists contains the elements (numbers [0 - GRID_SIZE]; GRID_SIZE = the length of a row or column on the board).

    Output: A list containing every sub-list.
    """
    result = []

    for line in grid:
        for element in line:
            result.append(element)

    return result

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
#
# SQ_GRID = 3
# GRID_SIZE = SQ_GRID ** 2
# number_of_zeros = 20
#
# unsolved_grid = generate_unsolved_sudoku(number_of_zeros, SQ_GRID, GRID_SIZE)
#
# print("\nboard after random element deletion (number of zeros = " + str(number_of_zeros) + "):")
# for line in unsolved_grid:
#     print(line)
#
# flat_unsolved_grid = flatten_grid(unsolved_grid)
# print("\nThe grid as a flat list:\n" + str(flat_unsolved_grid))