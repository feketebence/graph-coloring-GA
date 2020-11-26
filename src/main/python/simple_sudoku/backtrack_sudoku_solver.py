from print_util import print_9x9_board

## Imports needed for testing ##
from unsolved_sudoku_generator import generate_unsolved_sudoku
from unsolved_sudoku_generator import flatten_grid

#meg kell kapjuk az üres értékeket
def find_next_empty(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0: #ha 0 az illető érték akkor a "koordinátákat" térítjük vissza
                return i,j
    return None, None

def is_valid(puzzle, guess, row, column, grid):

    #sort ellenőrízzük
    row_vals = grid[row]
    if guess in row_vals: #ha a talalat benne van a sorban akkor az nem jo (return False)
        return False

    #oszlopot
    column_vals = []
    for i in range(9):
        column_vals.append(grid[i][column])

    if guess in column_vals: #ugyanugy ha az illeto oszlopban van benne
        return False

    #3X3-as mátrixokat nezzuk
    row_start = (row // 3) * 3
    column_start = (column // 3) * 3

    for i in range(row_start, row_start + 3):
        for j in range(column_start, column_start+3):
            if grid[i][j] == guess:
                return False

    return True

def solve_sudoku_backtrack(grid):

    #soron következő üres érték
    row, column = find_next_empty(grid) #ide az jon amit a find_next_empty fugvenyben visszateritettunk: i,j
    if row is None:
        return True

    for guess in range(1,10):
        if is_valid(grid, guess, row, column, grid): #ha helyes minden előbbi szempontból vizsgálva "guess",
                                               #akkor betesszük az illető helyre
            grid[row][column] = guess

            #backtracking rész
            if solve_sudoku_backtrack(grid):
                return True

        grid[row][column] = 0

    return False

### TESTING ###
SQ_GRID = 3
GRID_SIZE = SQ_GRID ** 2
number_of_zeros = 60

unsolved_grid = generate_unsolved_sudoku(number_of_zeros, 3, 9)

print("\nboard after random element deletion (number of zeros = " + str(number_of_zeros) + "):")
for line in unsolved_grid:
    print(line)

flat_unsolved_grid = flatten_grid(unsolved_grid)
print("\nThe grid as a flat list:\n" + str(flat_unsolved_grid))

print("\nThe pretty printed grid:")
print_9x9_board(unsolved_grid)

print("\nThe generated Sudoku is solvable: " + str(solve_sudoku_backtrack(unsolved_grid)))

print("\nThe pretty printed grid:")
print_9x9_board(unsolved_grid)