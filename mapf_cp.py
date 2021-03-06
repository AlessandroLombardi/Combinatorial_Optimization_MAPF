from utils.animation import movement_animation
from solvers.model_cp import solving_MAPF, run_CPLEX
from utils.environments import *

"""
This file allows to call to a specific graph the CP-based solution based on IBM CPLEX. Feel free to change graph, agents 
sizes etc..
"""

number_of_agents = 2
SIZE = 5
UPPER_BOUND = 70
SEED = 42

# e.g: an execution using the dungeon environment
"""
agents, edges, graph = environments(generate_dungeon, number_of_agents, SEED, rooms_num=2, rooms_size_min=3,
                                    rooms_size_max=3, corridor_length_min=2, corridor_length_max=2,
                                    seed=SEED)
"""

# e.g: an execution using the warehouse environment
agents, edges, graph = environments(generate_warehouse, [(51, 23), (2, 33), (36, 21), (3, 48), (29, 27)],
                                    SEED, rows=10, columns=7, shelf_length=3, corridor_width=1)

# Minimum shortest path is used in the algorithm to find the optimal number of layers
min_shortest_path, _ = min_max_shortest_path(graph, agents)

# The boilerplate code used here and in the test files to execute the algorithm cited in the paper
sep = "=" * 50
print(sep)
print("Step 1) Searching for optimal number of layers")
print(sep)
check, RET, num_layers, solve_time, memory_usage, number_of_conflicts, decisions = \
    solving_MAPF(agents, edges, UPPER_BOUND, min_shortest_path)

print(sep)
print("Step 2) Solving with %d layers" % num_layers)
print(sep)

paths = None
if check:
    _, mksp, solve_time, memory_usage, number_of_conflicts, decisions, paths = \
        run_CPLEX(edges, agents, RET, num_layers)
else:
    print("Unsatisfiable")

# Comment to not generate gif
if paths is not None:
    movement_animation(graph, paths, "./resources/warehouse.gif", seed=SEED)

# Uncomment to only visualize graph
"""
nx.draw(graph, with_labels=True)
plt.show()
"""
