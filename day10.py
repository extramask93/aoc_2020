from collections import deque, Counter
from typing import List, Set, FrozenSet, Mapping, Deque
from functools import cache
adapters = None

class Adapter:
    def __init__(self, joltage: int):
        self.rated_joltage = joltage
        self.children = []
        self.max_depth_child = None
        self.visited = False
    def __str__(self):
        return f"{self.rated_joltage=}, {self.children=} {self.max_depth_child=}"

def build_graph(adapters: Mapping[int, Adapter]):
    to_do: Deque[int] = deque()
    to_do.append(max(adapters.keys()))
    while to_do:
        current: int = to_do.popleft()
        for i in range(1,4):
            prev_joltage = current - i
            if prev_joltage in adapters:
                parent = adapters[prev_joltage]
                if not parent.visited:
                    to_do.append(prev_joltage)
                    parent.visited = True
                parent.children.append(current)

def build_max_depths(adapters):
    for adapter in adapters.values():
        adapter.max_depth_child = min(adapter.children, default=None)
        
def count_jolt_differences(start:int, adapters):
    current = adapters[start]
    differences = Counter()
    while current.max_depth_child:
        difference = current.max_depth_child - current.rated_joltage
        differences[difference] += 1
        current = adapters[current.max_depth_child]
    return differences[1], differences[3]
#top-up approach
@cache
def ways_to_reach_end(*,from_node: int):
    node = adapters[from_node]
    if not node.children:
        return 1
    total_ways = sum([ways_to_reach_end(from_node = child) for child in node.children])
    return total_ways




if __name__ == "__main__":
    #init data
    with open("inputs/day10.txt") as file:
        input = file.readlines()
    adapters = {int(line): Adapter((int(line))) for line in input}
    max_adapter_joltage = max(adapters.keys())
    adapters.update({0:Adapter(0), max_adapter_joltage+3: Adapter(max_adapter_joltage+3)})
    #build graph
    build_graph(adapters)
    build_max_depths(adapters)
    ones, threes = count_jolt_differences(0, adapters)
    print(ones*threes)
    print(ways_to_reach_end(from_node=0))
 
    

