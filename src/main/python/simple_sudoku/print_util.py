def print_9x9_board(grid):
    wall = "|--------------------------------|"

    print(wall)
    for i in range(9):
        for j in range(9):
            if ((i == 3 or i == 6) and j == 0):
                print(wall)
            if (j == 0 or j == 3 or j == 6):
                print("|", end = " ")
            print(" " + str(grid[i][j]), end=" ")
            if (j == 8):
                print("|")
    print(wall)