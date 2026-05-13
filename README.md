# The Torchbearer

**Student Name:** Luis Villalon
**Student ID:** 820437274
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting.

---

## Part 1: Problem Analysis

- **Why a single shortest-path run from S is not enough:**
  A single run only takes into account the cheapest path to individual chambers (nodes), it fails to consider the fuel needed to reach all the relic chambers. 

- **What decision remains after all inter-location costs are known:**
  The algorithm must decide in which order it will visit all the relic chambers that result in the minimum cumulative torch fuel cost from start to finish. 

- **Why this requires a search over orders (one sentence):**
  Due to the total fuel costs depending on the order of relic nodes visited, the algorithm must search through all possible orders of visited nodes to find the global minimum fuel cost route. 

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

| Source Node Type | Why it is a source |
|---|---|
| Spawn (start) node | Used to compute the shortest distance from the start to all relics and the exit. |
| Relic node | Used to compute the shortest distance between relics and from each relic to the exit. |

### Part 2b: Distance Storage

| Property | Your answer |
|---|---|
| Data structure name | Nested dictionary |
| What the keys represent | Outer key: source node, Inner key: destination node |
| What the values represent | Shortest-path distance from source to destination |
| Lookup time complexity | O(1) |
| Why O(1) lookup is possible | Dictionary hashing allows for a constant-time access by using a key |

### Part 2c: Precomputation Complexity

- **Number of Dijkstra runs:** k + 1, k = number of relic nodes
- **Cost per run:** O(m log n), m = number of edges, n = number of nodes
- **Total complexity:** O((k+1) m log n)
- **Justification (one line):** Dijkstra is ran with the spawn once and once with each of the k relics, each run costs O(m log n), so the total time complexity is O((k + 1) m log n).

---

## Part 3: Algorithm Correctness

### Part 3a: What the Invariant Means

- **For nodes already finalized (in S):**
  The shortest-path distance from the source to the current node is finalized and it will not change.

- **For nodes not yet finalized (not in S):**
  The distance is the shortest discovered path so far but may improve as more nodes are explored.

### Part 3b: Why Each Phase Holds

- **Initialization : why the invariant holds before iteration 1:**
  The source node has a distance of 0, and no paths have been discovered yet therefore all nodes have infinite distance.

- **Maintenance : why finalizing the min-dist node is always correct:**
  The node with the smallest distance is selected, and since all edge weights are nonnegative, no paths in the future can produce a shorter distance.

- **Termination : what the invariant guarantees when the algorithm ends:**
  All nodes have their shortest-path distances from the source computed correctly.

### Part 3c: Why This Matters for the Route Planner

Calculating the shortest-path distances correctly ensures that our route planner can correctly evaluate different orders of visitation and decide which path results in the minimum fuel cost route that visits all relics.

---

## Part 4: Search Design

### Why Greedy Fails

- **The failure mode:** A greedy approach will make its next decision based on local optimality when deciding to move to the next nearest relic, which can result in a suboptimal total fuel cost path.
- **Counter-example setup:** Suppose S→A = 1, S→B = 2, A→B = 4, B→A = 1, A→T = 1, and B→T = 3. Where A and B are relics that must both be visited. 
- **What greedy picks:** Greedy starts at S and chooses A first (cost 1), then goes A → B (cost 4), then B → T (cost 3) for a total cost of 1 + 4 + 3 = 8.
- **What optimal picks:** The optimal route is S → B → A → T, with a total cost of 2 + 1 + 1 = 4.
- **Why greedy loses:** A greedy approach will pick to visit node A first because it has a shorter distance locally, this leads to a more expensive finalized route, meanwhile starting with node B results in a total lower cost path.

### What the Algorithm Must Explore

- The algorithm must evaluate all possible orders of visiting the relic nodes to ensure the global minimum-cost route is chosen.

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | | | |
| Relics already collected | | | |
| Fuel cost so far | | | |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property | Your answer |
|---|---|
| Data structure chosen | |
| Operation: check if relic already collected | Time complexity: |
| Operation: mark a relic as collected | Time complexity: |
| Operation: unmark a relic (backtrack) | Time complexity: |
| Why this structure fits | |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** _Your answer (in terms of k)._
- **Why:** _One-line justification._

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** _Your answer here._
- **When it is used:** _Your answer here._
- **What it allows the algorithm to skip:** _Your answer here._

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** _Your answer here._
- **What the lower bound accounts for:** _Your answer here._
- **Why it never overestimates:** _Your answer here._

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- _Your answer here._

---

## References

> Bullet list. If none beyond lecture notes, write that.

- _Your references here._
