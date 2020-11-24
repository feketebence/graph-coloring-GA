import networkx as nx
import zmq
import time
import json

### just a bunch of example sudokus 
example_sudoku = [
    9, 6, 3, 0,
    0, 3, 7, 8,
    1, 2, 4, 0,
    0, 5, 2, 1
]

example_sudoku2 = [
    1, 2, 3, 9,
    6, 3, 0, 8,
    3, 2, 4, 0,
    7, 5, 2, 1
]

# example_sudoku2 = [
#     0, 0, 0, 8, 0, 1, 0, 0, 0,
#     0, 0, 0, 0, 0, 0, 4, 3, 0,
#     5, 0, 0, 0, 0, 0, 0, 0, 0,
#     0, 0, 0, 0, 7, 0, 8, 0, 0,
#     0, 0, 0, 0, 0, 0, 1, 0, 0,
#     0, 2, 0, 0, 3, 0, 0, 0, 0,
#     6, 0, 0, 0, 0, 0, 0, 7, 5,
#     0, 0, 3, 4, 0, 0, 0, 0, 0,
#     0, 0, 0, 2, 0, 0, 6, 0, 0
# ]

example_sudoku3 = [
    0, 0, 3, 0, 2, 0, 6, 0, 0,
    9, 0, 0, 3, 0, 5, 0, 0, 1,
    0, 0, 1, 8, 0, 6, 4, 0, 0,
    0, 0, 8, 1, 0, 2, 9, 0, 0,
    7, 0, 0, 0, 0, 0, 0, 0, 8,
    0, 0, 6, 7, 0, 8, 2, 0, 0,
    0, 0, 2, 6, 0, 9, 5, 0, 0,
    8, 0, 0, 2, 0, 3, 0, 0, 9,
    0, 0, 5, 0, 1, 0, 3, 0, 0
]


###
#   creating a collection of sudokus (just for testing purposes)

sudokus_in_list_form = []

sudokus_in_list_form.append(example_sudoku)
sudokus_in_list_form.append(example_sudoku2)
sudokus_in_list_form.append(example_sudoku3)

###
# FUNCTION DEFINITIONS
# TODO: create a separate module with these

def get_grid_size(sudoku_list):
    return int(len(sudoku_list) ** 0.5)

def get_sq_grid_size(sudoku_list):
    return int(len(sudoku_list) ** 0.25)

# generate sudoku board graph
def generate_sudoku_board_graph(GRID_SIZE):
    sudoku = nx.Graph()
    sudoku.add_nodes_from([
        (i, {"color": 0, "fixed": False}) for i in range(GRID_SIZE ** 2)
    ])

    return sudoku


def add_sudoku_board_egdes(sudoku, GRID_SIZE, SQ_GRID):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            
            row_neighbours = [(i * GRID_SIZE + j, i * GRID_SIZE + x) for x in range(GRID_SIZE) if x != j]
            col_neighbours = [(i * GRID_SIZE + j, x * GRID_SIZE + j) for x in range(GRID_SIZE) if x != i]
            
            sqr_i = (i // SQ_GRID) * SQ_GRID
            sqr_j = (j // SQ_GRID) * SQ_GRID
            sqr_neighbours = [(i * GRID_SIZE + j, a * GRID_SIZE + b) for a in range(sqr_i, sqr_i + SQ_GRID) for b in range(sqr_j, sqr_j + SQ_GRID) \
                            if (a != i or b != j)]
            
            unfiltered_neigh = row_neighbours + col_neighbours + sqr_neighbours
            filtered_neigh = list(set(unfiltered_neigh))
            
            sudoku.add_edges_from(filtered_neigh)
    
    return sudoku



# convert a given list "board" to networkx board 
def board_to_nx(sudoku, board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            idx = i * GRID_SIZE + j
            sudoku.nodes[idx]['idx'] = idx
            
            if board[idx] != 0:
                # 'fixed' means that the color of that node cannot be changed (during mutation or crossover)
                sudoku.nodes[idx]['fixed'] = True
                sudoku.nodes[idx]['color'] = board[idx]
    return sudoku

###


### Build dictionary from nodes, edges, GRID_SIZE, SQ_GRID ###

# TODO We can calculate GRID_SIZE and SQ_GRID from sudoku_list, change function header (use only sudoku_nx_graph and sudoku_list)

def build_sudoku_dict(sudoku, GRID_SIZE, SQ_GRID):                  
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


### Send the created dictionary to visualization process via TCP port ###
# TODO: Define a function for this
context = zmq.Context()

ip = 'localhost'
port = '5556'
address = "tcp://" + ip + ":" + port

#  Socket to talk to server (aka visualization process)
print("Connecting to visualization server…")
socket = context.socket(zmq.REQ)
socket.connect(address)

for i in range(0, 3):

    # 0. select a sudoku_list from the examples
    current_sudoku_list = sudokus_in_list_form[i]

    # 1. calculate the size of the whole grid (it's 9 for a regular sudoku) and the size of a smaller sub-grid ( it's 3 for a regular sudoku)
    GRID_SIZE = get_grid_size(current_sudoku_list) 
    SQ_GRID = get_sq_grid_size(current_sudoku_list)

    # 2. create sudoku graph with the nodes only (number of nodes = GRID_SIZE ^ 2)
    sudoku = generate_sudoku_board_graph(GRID_SIZE)

    # 2.1 add the edges to the graph created in the 2. step
    sudoku = add_sudoku_board_egdes(sudoku, GRID_SIZE, SQ_GRID)

    # 3. also adds 'fixed', 'color' and 'idx' attributes to nodes
    sudoku_nx_graph = board_to_nx(sudoku, current_sudoku_list)

    # TODO: Merge step 2 and 3 into a single step

    # 4. transform the generated graph into a dictionary (this is basically the pre-serialization step)
    sudoku_dictionary = build_sudoku_dict(sudoku_nx_graph, GRID_SIZE, SQ_GRID)

    # 5. serialize the sudoku_dictionary (create a JSON formatted data from it)
    message = json.dumps(sudoku_dictionary).encode('utf-8')

    # 6. send the serialized dict to the visualization process
    socket.send(message)
    print("Message nr. " + str(i) + " sent to " + address)

    # 7. wait for a reply from the other side (visualization process); while waiting, this thread is sleeping 
    # erre majd ki kell talaljunk valamit, ha kell varni a valaszra, akkor a GA nagyon sokat fog futni, 
    # elsore az jutott eszembe hogy a kigeneralt eredmenyeket bedobjuk egy tombbe es amikor valasz jon a vizu process-tol, akkor 
    # vesszuk ki a listabol a kovetkezo sudoku_dictionary, viszont igy nagyon sok dict fel fog gyulni

    # here the reply is encoded as a sequence of octets (byte string), so we need to decode it (byte str -> char str)
    reply = socket.recv()
    print("Received reply [ {} ]\n".format(reply.decode("utf-8")))

# send end signal
socket.send(b"END")
last_reply = socket.recv()
print("Last message from server: [ {} ]".format(last_reply.decode("utf-8")))
