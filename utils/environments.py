import networkx as nx
import random


def environments(graph_function, agents, agents_seed, **kwargs):
    """
    Create an environment from a NetworkX graph.

    :param graph_function: a function that returns a NetworkX graph, can be a customized one or one belonging to
    the wide range of predefined functions of the NetworkX library. Parameters are passed with the named
    argument **kwargs
    :param agents: the number of agents or the list containing origin and destination of each agent. In the former case
    the positions will be computed randomly.
    :param agents_seed: the random seed used for agents generation

    :return list of agents' positions, list of neighbors for each vertex and the minimum and maximum shortest path
    lengths

    :raise may generate an exception if the parameter of the NetworkX graph are not correct ot the number of agents is
    too big
    """

    graph = graph_function(**kwargs)

    graph = nx.convert_node_labels_to_integers(graph)

    edges = []

    for node, neighbors in graph.adj.items():
        edges.insert(node, set())
        edges[node].add(node)
        for neighbor, _ in neighbors.items():
            edges[node].add(neighbor)

    if type(agents) is int:
        agents = generate_agents(edges, agents, agents_seed)
    elif type(agents) is not list:
        raise Exception("agents must be an integer or a list of tuples.")
    else:
        for a in agents:
            if type(a) is not tuple:
                raise Exception("agents must be a list of tuples.")

    print("ENVIRONMENT: ")
    [print(str(node) + ": " + str(neighbors)) for node, neighbors in enumerate(edges)]
    print("AGENTS: ")
    print(agents)

    return agents, edges, graph


def generate_agents(edges, number_of_agents, seed=None):
    """
    Generate random origin and destination for a given number of agents

    :param edges: the list of neighbors for each vertex
    :param number_of_agents: the number of agents
    :return: a list of length number_of_agents, containing for each agent its origin and destination
    :param seed: the random seed

    :raise an exception when the number of agents is too big to fit in the graph
    """

    if number_of_agents * 2 > len(edges):
        raise ValueError("There are too many agents.")

    agents = []
    available_positions = list(range(len(edges)))
    random.seed(seed)

    while len(agents) < number_of_agents:
        agents.append((available_positions.pop(random.randrange(len(available_positions))),
                       available_positions.pop(random.randrange(len(available_positions)))))

    return agents


def min_max_shortest_path(graph, agents):
    """
    Compute and return the minimum and maximum shortest path.

    :param graph: the graph
    :param agents: the source and destination of each agent
    :return: the minimum and maximum shortest path
    """

    shortest_paths = [nx.shortest_path_length(graph, source=agent[0], target=agent[1]) for agent in agents]

    return min(shortest_paths), max(shortest_paths)


def grid_graph_with_obstacles(probability_obstacle, n, m, seed=None):
    """
    Create a grid graph removing some nodes as if they were obstacles

    :param probability_obstacle: probability to remove a node from the initial grd graph
    :param n: number of rows
    :param m: number of columns
    :param seed: the random seed
    :return: a grid graph with obstacles
    """

    graph = nx.grid_2d_graph(n, m)
    to_remove = []
    random.seed(seed)
    for n in graph:
        if random.random() <= probability_obstacle:
            to_remove.append(n)
    graph.remove_nodes_from(to_remove)

    return nx.convert_node_labels_to_integers(graph)


def generate_dungeon(rooms_num, rooms_size_min, rooms_size_max, corridor_length_min, corridor_length_max, seed=None):
    """
    Generate a NetworkX graph representing a dungeon or an indoor environment. Each room is connected with at least
    another. The corridors may start and end inside rooms, like a stairs between different floors.

    :param rooms_num: number of rooms
    :param rooms_size_min: minimum room's side length
    :param rooms_size_max: maximum room's side length
    :param corridor_length_min: minimum corridor's length
    :param corridor_length_max: maximum corridor's length
    :param seed: the random seed
    :return: a a NetworkX graph representing a dungeon or an indoor environment
    """

    if rooms_num <= 1 or rooms_size_min <= 1 or rooms_size_max <= 1 or corridor_length_min < 1 or\
            corridor_length_max < 0:
        raise ValueError("Some arguments are not correct")

    random.seed(seed)
    graph = nx.Graph()
    rooms = []
    for r in range(rooms_num):
        rooms.append(nx.grid_2d_graph(random.randint(rooms_size_min, rooms_size_max),
                                      random.randint(rooms_size_min, rooms_size_max)))
        graph = nx.disjoint_union(graph, rooms[r])

    links = [random.choice(list(i)) for i in nx.connected_components(graph)]

    for lnk in range(len(links) - 1):
        path = []
        corridor_length = range(random.randint(corridor_length_min, corridor_length_max))
        for p in corridor_length:
            path.append(max(graph.nodes) + 1 + p)

        nx.add_path(graph, [links[lnk]] + path + [links[lnk + 1]])

    return nx.convert_node_labels_to_integers(graph)


def generate_warehouse(rows, columns, shelf_length, corridor_width):
    """
    Generate a warehouse style graph
    :param rows: grid number of rows, direction of the shelves.
    :param columns: grid number of columns, bigger at least of 2 than the shelf length.
    :param shelf_length: length of the shelf
    :param corridor_width: distance between shelves
    :return: graph
    """
    if columns <= 0 or rows <= 0:
        raise ValueError("Warehouse size is not correct.")
    if shelf_length <= 0 or shelf_length > columns - 2:
        raise ValueError("Shelf size is not correct. At least a vertical corridor of width 1 must exist in left and "
                         "right sides.")
    if corridor_width <= 0 or corridor_width + 1 > rows - 2:
        raise ValueError("The corridor width is not correct.")

    corridors_num = rows // (corridor_width + 1)
    y_offset = (columns - shelf_length) // 2
    to_remove = []
    for c in range(corridors_num):
        for i in range(y_offset, y_offset + shelf_length):
            to_remove.append((i, 1 + (1 + corridor_width) * c))

    graph = nx.grid_2d_graph(columns, rows)
    graph.remove_nodes_from(to_remove)

    return nx.convert_node_labels_to_integers(graph)
