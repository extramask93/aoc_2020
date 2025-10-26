import re
from typing import List, Tuple

ranges_pattern = re.compile(r".*:\s([\d\-]+)\s+or\s+([\d\-]+)")

def merge_ranges(ranges: List[Tuple[int,int]]) -> List[Tuple[int,int]]:
    current_range = ranges[0]
    result = list()
    for r in ranges[1:]:
        if r[0] < current_range[1]:
            current_range[0] = min(current_range[0], r[0])
            current_range[1] = max(current_range[1], r[1])
        else:
            result.append(current_range)
            current_range = r
    result.append(current_range)
    return result
def parse_rules(s:str) -> List[Tuple[int,int]]:
    ranges = []
    for line in s.splitlines():
        m = ranges_pattern.search(line)
        for r in m.group(1,2):
            intr = list(map(int, r.split("-")))
            ranges.append(intr)
    return sorted(ranges)
def parse_nearby_tickets(s: str) -> List[int]:
    all_tickets = []
    for line in s.splitlines()[1:]:
        all_tickets.extend(int(x) for x in line.split(","))
    return all_tickets
def find_tickets_outside_of_range(ranges: List[Tuple[int,int]], tickets: List[int]) -> List[int]:
    result: List[int] = []
    for ticket in tickets:
        found = False
        for range in ranges:
            if ticket >= range[0] and ticket<=range[1]:
                found = True
        if not found:
            result.append(ticket)
    return result




if __name__ == "__main__":
    with open("inputs/day16.txt", "r") as f:
        content = f.read()
    rules, ticket, nearby = content.split("\n\n")
    ranges = parse_rules(rules)
    merged_ranges = merge_ranges(ranges)
    tickets = parse_nearby_tickets(nearby)
    invalid_tickets = find_tickets_outside_of_range(merged_ranges, tickets)
    print(sum(invalid_tickets))
    # PART 2
    valid_tickets = set(tickets).difference_update(invalid_tickets)
