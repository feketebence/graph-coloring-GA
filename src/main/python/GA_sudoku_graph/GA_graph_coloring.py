### IMPORTS ###
# setting up the import form the ../simple_sudoku folder
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir + "/simple_sudoku")

from unsolved_sudoku_generator import generate_unsolved_sudoku

# setting up the import form the ../utils folder
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir + "/utils")

from print_util import print_9x9_board
from grid_transforms import flatten_grid
### END OF IMPORTS ###

### Sudoku grid constants ###
SQ_GRID = 3
GRID_SIZE = SQ_GRID ** 2
number_of_zeros = 60 # the number of 'empty' cells on the generated board

## Generating an unsolved grid
unsolved_grid = generate_unsolved_sudoku(number_of_zeros, SQ_GRID, GRID_SIZE)

## printing the generated (unsolved) grid in different formats
# line by line
for line in unsolved_grid:
    print(line)

# flat list (ez a forma kell a GA-nak)
flat_unsolved_grid = flatten_grid(unsolved_grid)
print("\nThe grid as a flat list:\n" + str(flat_unsolved_grid))

# sudoku board with walls
print("\nThe pretty printed grid:")
print_9x9_board(unsolved_grid)

# ez csak az egyik random kigeneralt grid, csak azert tettem ide, hogy ezzel tesztelgesd hogy jo mukodik-e a GA
# es ne kelljen minden alkalommal ujat generalni
example_grid = [
    3, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 1, 0, 0, 0, 0, 4, 5,
    0, 2, 0, 0, 0, 1, 7, 0, 0,
    2, 0, 0, 6, 0, 8, 0, 0, 0,
    0, 0, 0, 4, 0, 0, 0, 0, 0,
    0, 0, 0, 3, 0, 0, 0, 0, 0,
    0, 8, 0, 0, 7, 3, 0, 0, 0,
    0, 0, 9, 2, 0, 4, 6, 0, 0,
    0, 4, 0, 0, 0, 0, 0, 3, 0
]

# Ezt a board_to_nx verziot hasznald, ugyan az mint a tied, csak felrakja minden node-ra explicit az indexet is mint egy kulon attributum (ez szukseges a vizu resznel)
# convert a given list "board" to networkx board
def board_to_nx(sudoku, board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            idx = i * GRID_SIZE + j
            sudoku.nodes[idx]['idx'] = idx # csak ezt a sort adtam hozza

            if board[idx] != 0:
                # 'fixed' means that the color of that node cannot be changed (during mutation or crossover)
                sudoku.nodes[idx]['fixed'] = True
                sudoku.nodes[idx]['color'] = board[idx]
    return sudoku

# The floor is yours. peppa