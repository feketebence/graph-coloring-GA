### IMPORTS ###
# setting up the import form the ../simple_sudoku folder
import os, sys, inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir + "/simple_sudoku")

from unsolved_sudoku_generator import generate_unsolved_sudoku

# setting up the import form the ../utils folder
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir + "/utils")

from print_util import print_9x9_board
from grid_transforms import flatten_grid

import numpy as np
import random
import networkx as nx
import copy

import zmq
import time
import json

### END OF IMPORTS ###

# VARIABLES FOR ZMQ
# TODO: Define a function for this
context = zmq.Context()

ip = 'localhost'
port = '5556'
address = "tcp://" + ip + ":" + port

#  Socket to talk to server (aka visualization process)
print("Connecting to visualization server…")
socket = context.socket(zmq.REQ)
socket.connect(address)

### Sudoku grid constants ###
SQ_GRID = 3
GRID_SIZE = SQ_GRID ** 2
number_of_zeros = 60  # the number of 'empty' cells on the generated board

# ## Generating an unsolved grid
# unsolved_grid = generate_unsolved_sudoku(number_of_zeros, SQ_GRID, GRID_SIZE)

# ## printing the generated (unsolved) grid in different formats
# # line by line
# for line in unsolved_grid:
#     print(line)

# # flat list (ez a forma kell a GA-nak)
# flat_unsolved_grid = flatten_grid(unsolved_grid)
# print("\nThe grid as a flat list:\n" + str(flat_unsolved_grid))

# # sudoku board with walls
# print("\nThe pretty printed grid:")
# print_9x9_board(unsolved_grid)

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

# ezzel a táblával könnyebb a tesztelés, nem kell órákat várni, hogy megoldja
example_2 = [
    8, 0, 2, 0, 5, 0, 7, 0, 1,
    0, 0, 7, 0, 8, 2, 4, 6, 0,
    0, 1, 0, 9, 0, 0, 0, 0, 0,
    6, 0, 0, 0, 0, 1, 8, 3, 2,
    5, 0, 0, 0, 0, 0, 0, 0, 9,
    1, 8, 4, 3, 0, 0, 0, 0, 6,
    0, 0, 0, 0, 0, 4, 0, 2, 0,
    0, 9, 5, 6, 1, 0, 3, 0, 0,
    3, 0, 8, 0, 9, 0, 6, 0, 7,
]

def build_sudoku_dict(sudoku, GRID_SIZE):
    SQ_GRID = int(GRID_SIZE ** 0.5)

    # for the visualization step, we'll need the color (which is the value) of a given node 
    nodes_with_color = []
    for i in sudoku.nodes:
        nodes_with_color.append(sudoku.nodes[i])

    # all the information we need to visualize the graph (create new  graph or update an existing one)
    sudoku_dict = {
        'GRID_SIZE': GRID_SIZE,
        'SQ_GRID': SQ_GRID,
        'sudoku_graph': {
            'nodes': nodes_with_color,
            'edges': list(sudoku.edges)
        }
    }

    print("\nThe whole sudoku dictionary: \n", sudoku_dict)

    return sudoku_dict

# Ezt a board_to_nx verziot hasznald, ugyan az mint a tied, csak felrakja minden node-ra explicit az indexet is mint egy kulon attributum (ez szukseges a vizu resznel)
# convert a given list "board" to networkx board
def board_to_nx(sudoku, board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            idx = i * GRID_SIZE + j
            sudoku.nodes[idx]['idx'] = idx  # csak ezt a sort adtam hozza

            if board[idx] != 0:
                # 'fixed' means that the color of that node cannot be changed (during mutation or crossover)
                sudoku.nodes[idx]['fixed'] = True
                sudoku.nodes[idx]['color'] = board[idx]
    return sudoku


def init_board():
    sudoku = nx.Graph()
    sudoku.add_nodes_from([
        (i, {"color": 0, "fixed": False}) for i in range(81)
    ])

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            row_neighbours = [(i * GRID_SIZE + j, i * GRID_SIZE + x) for x in range(GRID_SIZE) if x != j]
            col_neighbours = [(i * GRID_SIZE + j, x * GRID_SIZE + j) for x in range(GRID_SIZE) if x != i]

            sqr_i = (i // SQ_GRID) * SQ_GRID
            sqr_j = (j // SQ_GRID) * SQ_GRID
            sqr_neighbours = [(i * GRID_SIZE + j, a * GRID_SIZE + b) for a in range(sqr_i, sqr_i + SQ_GRID) for b in
                              range(sqr_j, sqr_j + SQ_GRID) \
                              if (a != i or b != j)]

            unfiltered_neigh = row_neighbours + col_neighbours + sqr_neighbours
            filtered_neigh = list(set(unfiltered_neigh))

            sudoku.add_edges_from(filtered_neigh)

    return sudoku


'''
    A tábla egy sorát úgy fogjuk fel, mint az 1-től 9-ig levő számok egy permutációja.
    Ez segít az algoritmusnak hamarabb konvergálni egy esetleges megoldás fele.
'''


def create_population(n, base_board, max_color):
    copies = [copy.deepcopy(base_board) for _ in range(n)]

    for graph in copies:
        graph.graph['fitness'] = None

        for i in range(max_color):

            row_colors = [graph.nodes[i * max_color + j]['color'] for j in range(max_color)]
            possible_colors = [(k + 1) for k in range(max_color) if not (k + 1) in row_colors]

            for j in range(max_color):
                if graph.nodes[i * max_color + j]['fixed'] == False:
                    color = random.choice(possible_colors)
                    graph.nodes[i * max_color + j]['color'] = color
                    possible_colors.remove(color)

    return copies


def fitness(population):
    for individual in population:
        if individual.graph['fitness'] != None:
            continue

        fitness = 0
        for edge in individual.edges:
            if individual.nodes[edge[0]]['color'] == individual.nodes[edge[1]]['color']:
                fitness -= 1

        individual.graph['fitness'] = fitness

    return population


def swap_mutation(population, pm, max_color):
    for instance in population:
        mut_hap = False

        for i in range(max_color):
            for j in range(max_color):
                node = i * max_color + j
                rn_node = random.randint(i * max_color, (i + 1) * max_color - 1)

                if instance.nodes[node]['fixed'] or instance.nodes[rn_node]['fixed']:
                    continue
                else:
                    if random.random() <= pm:
                        instance.nodes[node]['color'], instance.nodes[rn_node]['color'] = instance.nodes[rn_node][
                                                                                              'color'], \
                                                                                          instance.nodes[node]['color']
                        mut_hap = True
        if mut_hap:
            instance.graph['fitness'] = None

    return population


def tournament_selection(population, k, possible):
    best = random.choice(possible)

    for _ in range(k):
        rnd_idx = random.choice(possible)
        if population[rnd_idx].graph['fitness'] >= population[best].graph['fitness']:
            best = rnd_idx

    return best


def crossover(p1, p2, pc):
    o1, o2 = copy.deepcopy(p1), copy.deepcopy(p2)

    if random.random() > pc:
        return o1, o2

    size = int(len(o1.nodes) ** 0.5)
    for i in range(size):
        if i % 2:
            for j in range(size):
                node = i * size + j
                o1.nodes[node]['color'], o2.nodes[node]['color'] = o2.nodes[node]['color'], o1.nodes[node]['color']

    o1.graph['fitness'] = None
    o2.graph['fitness'] = None

    return o1, o2


def elitism_selection(population, N):
    new_pop = []

    while len(new_pop) != N:
        best = population[0]

        for individual in population:
            if individual.graph['fitness'] > best.graph['fitness']:
                best = individual

        new_pop.append(best)
        population.remove(best)

    return new_pop


# check if any of the individuals is a complete solution
def solution(population):
    for ind in population:
        if ind.graph['fitness'] == 0:
            return True
    return False


# find the best individual of a population
def find_best(population):
    best = population[0]

    for ind in population:
        if ind.graph['fitness'] > best.graph['fitness']:
            best = ind

    return best


def genetic_algorithm(sudoku):
    GRID_SIZE = 9

    # initialize GA parameters
    POP_SIZE = 100
    P_MUTATION = 0.03
    P_CROSSOVER = 0.9
    N_MATING_POOL = 10
    # selection pressure for tournament selection
    S_PRESSURE = 10
    MAX_GENER = 600

    generation = 0

    # init population
    population = create_population(POP_SIZE, sudoku, GRID_SIZE)
    population = fitness(population)

    while not solution(population):

        # select parents
        possible_parents = [i for i in range(POP_SIZE)]
        parents = []

        for _ in range(N_MATING_POOL):
            p1 = tournament_selection(population, S_PRESSURE, possible_parents)
            possible_parents.remove(p1)
            p2 = tournament_selection(population, S_PRESSURE, possible_parents)

            possible_parents.remove(p2)

            parents.append((p1, p2))

        # crossover
        for (p1, p2) in parents:
            o1, o2 = crossover(population[p1], population[p2], P_CROSSOVER)
            # add new offspring to population
            population += [o1, o2]

        # mutation
        population = swap_mutation(population, P_MUTATION, GRID_SIZE)

        # evaluate fitness
        population = fitness(population)

        # select survivors
        population = elitism_selection(population, POP_SIZE)

        # print best score
        if generation % 100 == 0:
            best = find_best(population)
            print("Generation {}. best score: {}".format(generation, best.graph['fitness']))
        

        generation += 1

        if generation == MAX_GENER:
            break

    return find_best(population), generation

def send_sudoku(sudoku, GRID_SIZE, socket, address):
    initial_sudoku_dictionary = build_sudoku_dict(sudoku, GRID_SIZE)
    message = json.dumps(initial_sudoku_dictionary).encode('utf-8')
    socket.send(message)
    print("Sudoku was sent to " + address)

    reply = socket.recv()
    print("Received reply [ {} ]\n".format(reply.decode("utf-8")))

def send_end_signal(socket):
    socket.send(b"END")
    last_reply = socket.recv()
    print("Last message from server: [ {} ]".format(last_reply.decode("utf-8")))

sudoku = init_board()
sudoku = board_to_nx(sudoku, example_2)

# send initial sudoku to visualizer component
send_sudoku(sudoku, GRID_SIZE, socket, address)

solution, n_generations = genetic_algorithm(sudoku)
print(n_generations)

# send solution to visualizer component
send_sudoku(solution, GRID_SIZE, socket, address)

send_end_signal(socket)
