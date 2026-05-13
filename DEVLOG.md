# Development Log – The Torchbearer

**Student Name:** Luis Villalon
**Student ID:** 820437274

---

## Entry 1 – [05/09/2026]: Initial Plan

I will read the ASSIGNMENT.md file to understand the problem and the requirements for code design better. I plan to answer questions 1 through 3 in the README.md file before I start to code to have a better conceptual understanding on how to implement the necessary algorithm. I plan find out what data structures I will have to use to store the path distances, visited relic tracking, and best-route tracking. I expect to have a hard time figuring out how to store every possible order of visits for the relic nodes to evaluate for the optimal route. 

---

## Entry 2 – [05/12/2026]: Implementing Dijkstra's algorithm

When implementing Dijkstra's algorithm it was returning an incorrect distance for some paths. This would result in my distance table holding wrong values which then led to the route optimization step to return incorrect values. The issue was that I was not handling outdated entries in the prioroity queue. I was able to fix this by implementing a conditional statement (if curr_dist > dist[curr_node] ==> continue) that allows the algorithm to skip outdated entries and only expand the shortest known path.


---

## Entry 3 – [05/13/2026]: Part 4-6: Pruning, Recursion, Backtrack

When implementing the _explore function I ran into an issue where the function was returning incorrect values for the relic orders and total costs. I found the problem was being caused because the state was not being properly restored because I was not taking into account backtracking. I was not re-adding relics into the relics_remaining set after each recursive call. I was able to fix this by removing the relic form the current path and adding it back to relics_remaining after each recursive call.

---

## Entry 4 – [05/14/2026]: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

_Your entry here._

---

## Final Entry – [05/14/2026]: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | |
| Part 2: Precomputation Design | |
| Part 3: Algorithm Correctness | |
| Part 4: Search Design | |
| Part 5: State and Search Space | |
| Part 6: Pruning | |
| Part 7: Implementation | |
| README and DEVLOG writing | |
| **Total** | |
