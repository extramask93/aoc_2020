from pathlib import Path
from typing import List
from itertools import permutations

def read_input_values(path: Path) -> List[str]:
    with path.open("r") as file:
        return file.readlines()
        
def target_addends(values: List[int], target: int) -> tuple[int]| None:
    seen = set()
    for val in values:
        complement = target-val
        if complement in seen:
            return val, complement
        seen.add(val)
    return None

if __name__ == "__main__":
    values = [int(x) for x in read_input_values(Path("inputs") / "day1.txt")]
    a,b = target_addends(values, 2020)
    print(f"First = {a*b}")
    for i, value in enumerate(values):
        addends = target_addends(values[i:], 2020-value)
        if addends is not None:
            print(f"Second = {value*addends[0]*addends[1]}")
            break
            

        