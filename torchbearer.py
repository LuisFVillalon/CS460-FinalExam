"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Luis Villalon
Student ID: 820437274

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.

    TODO
    """
    q1 = "A single run only takes into account the cheapest path to individual chambers (nodes), it fails to consider the fuel needed to reach all the relic chambers."
    q2 = "The algorithm must decide in which order it will visit all the relic chambers that result in a the minimum cumulative torch fuel cost from start to finish."
    q3 = "Due to the total fuel costs depending on the order nodes are visited, the algorithm must search through all possible orders of visited nodes to find the global minimum fuel cost route."
    ans = q1 + " " + q2 + " " + q3


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.

    TODO
    """
    unique_nodes = [spawn]
    for node in relics:
        if node not in unique_nodes:
            unique_nodes.append(node)
    return unique_nodes

def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').

    TODO
    """
    dist = {}

    # initiliaze all distances to infinity
    for node in graph:
        dist[node] = float('inf')

    # distance to source is zero
    dist[source] = 0

    # min-heap: (distance, node), lowest values priority queue
    heap = [(0, source)]

    while heap:
        curr_dist, curr_node = heapq.heappop(heap)
        # skip paths that cost more fuel than the path that is currently stored
        if curr_dist > dist[curr_node]:
            continue
        # traverse the neighbor nodes
        for neighbor, cost in graph.get(curr_node, []):
            if neighbor not in dist:
                dist[neighbor] = float('inf')
            new_dist = curr_dist + cost
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    return dist

def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.

    TODO
    """
    dist_table = {}
    sources = select_sources(spawn, relics, exit_node)
    for source in sources:
        dist_table[source] = run_dijkstra(graph, source)
    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.

    TODO
    """
    qa1 = "The shortest-path distance from the source to the current node is finalized and it will not change."
    qa2="The distance is the shortest discovered path so far but may improve as more nodes are explored."
    qb1="The source node has a distance of 0, and no paths have been discovered yet therefore all node have infinite distance."
    qb2="The node with the smallest distance is selected, and since all edge weights are nonnegative, no paths in the future can produce a shorter distance."
    qb3="All nodes have their shortest-path distances from the source computed correctly."
    qc1="Calculating the shortest-path distances correctly ensures that our route planner can correctly evaluate different orders of visitation and decide which path results in the minimum fuel cost route that visits all relics."
    ans = qa1 + " " + qa2 + " " + qb1 + " " + qb2 + " " + qb3 + " " + qc1
    return ans


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.

    TODO
    """
    q1="A greedy approach will make its next decision based on local optimality when deciding to move to the next nearest relic, which can result in a suboptimal total fuel cost path."
    q2="Suppose S→A = 1, S→B = 2, A→B = 4, B→A = 1, A→T = 1, and B→T = 3. Where A and B are relics that must both be visited."
    q3="Greedy starts at S and chooses A first (cost 1), then goes A → B (cost 4), then B → T (cost 3) for a total cost of 1 + 4 + 3 = 8."
    q4="The optimal route is S → B → A → T, with a total cost of 2 + 1 + 1 = 4."
    q5="A greedy approach will pick to visit node A first because it has a shorter distance locally, this leads to a more expensive finalized path, meanwhile starting with node B results in a total lower cost path."
    q6="The algorithm must evaluate all possible orders of visiting the relic nodes to ensure the global minimum-cost path is chosen."
    ans = q1 + " " + q2 + " " + q3 + " " + q4 + " " + q5 + " " + q6
    return ans


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    # track which relics still need to be visited
    relics_remaining = set(relics)
    # tracks the order of relics chosen so far
    relics_visited_order = []
    # no fuel spent yet at spawn
    cost_so_far = 0
    # stores the best complete route found so far
    # best[0] = minimum fuel cost, best[1] = best relic order
    best = [float('inf'), []]

    _explore(dist_table, spawn, relics_remaining, relics_visited_order, cost_so_far, exit_node, best)

    return best[0], best[1]

def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.

    TODO
    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    pass


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    pass


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
