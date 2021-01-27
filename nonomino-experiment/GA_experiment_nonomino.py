import numpy as np
import networkx as nx

import copy
import time
from datetime import datetime
import random
import sys

GRID_SIZE = 9
SQ_GRID = int(GRID_SIZE ** 0.5)
max_gen=10_000

def init_nonomino_board(board_group_vals):
    nonomino = nx.Graph()
    
    # adding nodes
    nonomino.add_nodes_from([
        (i, {"color": 0, "fixed": False}) for i in range(81)
    ])

    unfiltered_neigh = []
    # Adding edges 
    # adding traditional row and column edges
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            # 
            row_neighbours = [(i * GRID_SIZE + j, i * GRID_SIZE + x) for x in range(GRID_SIZE) if x != j]
            col_neighbours = [(i * GRID_SIZE + j, x * GRID_SIZE + j) for x in range(GRID_SIZE) if x != i]

            unfiltered_neigh += row_neighbours + col_neighbours

    # adding nonomino specific edges
    nonomino_neighbours = []
    for i in range(0,len(board_group_vals)):
            for j in range(len(board_group_vals)):
                if board_group_vals[i] == board_group_vals[j] and i != j:
                    nonomino_neighbours.append((i, j))

    unfiltered_neigh += nonomino_neighbours

    # delete multiple edges between two nodes
    filtered_neigh = list(set(unfiltered_neigh))
    
    # add the edges to the graph
    nonomino.add_edges_from(filtered_neigh)
    
    return nonomino

# convert a given list "board" to networkx board 
def board_to_nx(sudoku, board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            idx = i * GRID_SIZE + j
            
            if board[idx] != 0:
                # 'fixed' means that the color of that node cannot be changed (during mutation or crossover)
                sudoku.nodes[idx]['fixed'] = True
                sudoku.nodes[idx]['color'] = board[idx]
    return sudoku

def print_board(nx_board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            print(nx_board.nodes[i * GRID_SIZE + j]['color'], end=' ')
        print()

# GA related functions #
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
                        instance.nodes[node]['color'], instance.nodes[rn_node]['color'] = instance.nodes[rn_node]['color'], instance.nodes[node]['color']
                        mut_hap = True
        if mut_hap:
            instance.graph['fitness'] = None
            
    return population

def tournament_selection(population, k, possible):
    
    best = random.choice(possible)
    
    for i in range(k):
        rnd_idx = random.choice(possible)
        if population[rnd_idx].graph['fitness'] >= population[best].graph['fitness']:
            best = rnd_idx
            
    return best

"""
    Uniform crossover when a row on the table is a permutation
    Specific to the sudoku problem.
"""

def crossover(p1, p2, pc):
    o1, o2 = copy.deepcopy(p1), copy.deepcopy(p2)
    
    if random.random() > pc:
        return o1, o2
    
    size = int(len(o1.nodes) ** 0.5)
    for i in range(size):
        if i%2:
            for j in range(size):
                node = i * size + j
                o1.nodes[node]['color'], o2.nodes[node]['color'] = o2.nodes[node]['color'], o1.nodes[node]['color']
                
    o1.graph['fitness'] = None
    o2.graph['fitness'] = None
    
    return o1, o2

# choose N best individuals from population
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

def genetic_algorithm(sudoku,
                      create_fn, fitness_fn, selection_fn, solution_fn,
                      crossover_fn, mutation_fn, survivor_fn, best_fn,
                      # optional params
                      grid_size=9, pop_size=11, p_m=0.03, p_c=0.9,
                      mating_pool=2, s_pres=7, max_gen=500_000):
    
    GRID_SIZE = grid_size
    
    # initialize GA parameters
    POP_SIZE = pop_size
    P_MUTATION = p_m
    P_CROSSOVER = p_c
    N_MATING_POOL = mating_pool
    # selection pressure for tournament selection
    S_PRESSURE = s_pres
    MAX_GENER = max_gen

    generation = 0

    # init population
    population = create_fn(POP_SIZE, sudoku, GRID_SIZE)
    population = fitness_fn(population)

    while not solution_fn(population):
    
        # select parents
        possible_parents = [i for i in range(POP_SIZE)]
        parents = []
    
        for i in range(N_MATING_POOL):
            p1 = selection_fn(population, S_PRESSURE, possible_parents)
            possible_parents.remove(p1)
            p2 = selection_fn(population, S_PRESSURE, possible_parents)
        
            possible_parents.remove(p2)

            parents.append((p1, p2))
        
        # crossover
        for (p1, p2) in parents:
            o1, o2 = crossover_fn(population[p1], population[p2], P_CROSSOVER)
            # add new offspring to population
            population += [o1, o2]
        
        # mutation
        population = mutation_fn(population, P_MUTATION, GRID_SIZE)
    
        # evaluate fitness
        population = fitness_fn(population)
    
        # select survivors
        population = survivor_fn(population, POP_SIZE)
    
        # print best score
        if generation % 10 == 0:
            best = best_fn(population)
            print("Generation {}. best score: {}".format(generation, best.graph['fitness']))
    
        generation += 1
    
        if generation == MAX_GENER:
            break
            
    return find_best(population), generation
# END OF FUNCTION DEFINITIONS


board_color_vals = []
board_group_vals = []

# input format for nonomino: <color_value>,<group_value>
input_file_path = str(sys.argv[1])
with open(input_file_path, "r") as n_file:
    lines = n_file.readlines()
    
print('Reading input from file:', input_file_path, '\n')
i = 1
for line in lines:
    line = line.strip()
    color_value, group_value = line.split(",")
    
    board_color_vals.append(int(color_value))
    board_group_vals.append(int(group_value))
    
    print(str(i) + ": \t" + line + " [color_value:" + color_value + ", group_value: " + group_value + "]")
    i+=1


nonomino = init_nonomino_board(board_group_vals)
nonomino = board_to_nx(nonomino, board_color_vals)

zeros_count = 0

for elem in board_color_vals:
    if elem == 0:
        zeros_count += 1
print("Number of zeros (empty cells) in board:", zeros_count)

print("\nExperimenting on the following Nonomino board:")
print_board(nonomino)

print("\n---------=== BEGINNING OF EXPERIMENTS ===---------")
print("-\tStarted on: ", datetime.now(), ' -')
print("--------------------------------------------------")

print('max_gen =', max_gen)

# EXPERIMENT
n_generations = []
time_run = []
N_EXPERIMENTS = 10

pop_size = [10, 20, 30]
p_mutation = [0.03, 0.07]
p_crossover = [0.9, 1.]
selection_pressure = [5, 10]

for p_size in pop_size:
    for p_m in p_mutation:
        for p_c in p_crossover:
            for s_pres in selection_pressure:
                print("\nParameters: [ pop_size={}, p_mutation={}, p_crossover={}, selection_pressure={} ]".format(str(p_size), str(p_m), 
                                                            str(p_c), str(s_pres)))
                
                for i in range(N_EXPERIMENTS):
                    stime = time.time()
                    print("\nExperiment {}:".format(str(i)))
                    sol, n_gens = genetic_algorithm(nonomino, create_population, fitness,
                               tournament_selection, solution, crossover,
                               swap_mutation, elitism_selection, find_best,
                                pop_size=p_size, p_m=p_m, p_c=p_c, s_pres=s_pres, max_gen=max_gen)
                    
                    time_run.append(time.time() - stime)
                    n_generations.append(n_gens)
                
                mean_gen = sum(n_generations) / len(n_generations)
                std_gen = (sum([(x - mean_gen) ** 2 for x in n_generations]) / (len(n_generations) - 1)) ** 0.5
                print("Mean: {}; Std: {}".format(str(mean_gen), str(std_gen)))
                
                mean_time = sum(time_run) / len(time_run)
                std_time = (sum([(x - mean_time) ** 2 for x in time_run]) / (len(time_run) - 1)) ** 0.5
                print("Time mean: {}; Std: {}".format(str(mean_time), str(std_time)))

print("\n------------=== END OF EXPERIMENTS ===------------")
print("-\tEnded on: ", datetime.now(), ' -')
print("--------------------------------------------------")