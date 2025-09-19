import re
from functools import cache
from collections import deque
from typing import List, Dict, TextIO
class Bagger:
    ROOT_BAG_RE = re.compile(r"([\w\s]+)bags contain (.*)")
    CONTAINED_BAGS_RE = re.compile(r"(\d+) ([\w\s]+) bags*")
    def __init__(self, bags: Dict[str, List[str]]):
        self.bags = bags
    @classmethod
    def from_buffer(cls, buffer: TextIO) -> "Bagger":
        bags: Dict[str,List[str]]={}
        for line in buffer:
            match = cls.ROOT_BAG_RE.search(line)
            root_bag = match.group(1).strip()
            contained = []
            for bag in match.group(2).split(","):
                bag_match = cls.CONTAINED_BAGS_RE.search(bag)
                if bag_match:
                    amount = int(bag_match.group(1))
                    name = bag_match.group(2)
                    contained.extend(amount*[name])
            bags[root_bag]= contained
        return cls(bags)
    def count_bags_that_can_hold_shiny(self) -> int:
        return sum(self.can_hold_shiny_bag(bag) for bag in self.bags)
    @cache
    def can_hold_shiny_bag(self, bag) -> bool:
        contained_bags: List[str] = self.bags[bag]
        #direct hold
        if "shiny gold" in contained_bags:
            return True
        #indirect hold
        return any(self.can_hold_shiny_bag(b) for b in contained_bags)
    def count_nested_bags(self, bag)->int:
        bags_to_check = deque([bag])
        held_bags = -1 #we put shiny gold on the list, but it can't be counted as total
        while bags_to_check:
            current_bag:str = bags_to_check.popleft()
            held_bags +=1
            bags_to_check.extend(self.bags[current_bag])
        return held_bags


if __name__ == "__main__":
    with open("inputs/day7.txt") as file:
        bagger = Bagger.from_buffer(file)
    print(bagger.count_bags_that_can_hold_shiny())
    print(bagger.count_nested_bags("shiny gold"))
