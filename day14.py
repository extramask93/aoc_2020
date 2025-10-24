from typing import List, Tuple
from collections import namedtuple
import re
inp = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""
memory_pattern = re.compile(r"mem\[(\d+)\]\s+=\s+(\d+)")
mask_pattern = re.compile(r"mask\s+=\s+([X01]+)")
MemoryValue = namedtuple("MemoryValue", ["address", "value"])

def mask_parser(mask: str):
    m = mask_pattern.search(mask)
    mask = m.group(1)
    and_mask = mask.replace("X","1")
    or_mask = mask.replace("X", "0")
    return int(and_mask,2), int(or_mask,2)
def memory_parser(mem: str) -> None | MemoryValue:
    m = memory_pattern.search(mem)
    return MemoryValue(*map(int,m.group(1,2)))

if __name__ == "__main__":
    memory = dict()
    or_mask = 0
    and_mask = -1
    with open("inputs/day14.txt", "r") as f:
        for line in f:
            line = line.strip()
            if "mask" in line:
                and_mask, or_mask = mask_parser(line)
            else:
                mem = memory_parser(line)
                memory[mem.address] = (mem.value & and_mask) | or_mask
    print(sum(memory.values()))
