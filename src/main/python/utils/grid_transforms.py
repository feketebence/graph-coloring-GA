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