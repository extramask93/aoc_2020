from typing import List, Optional, Tuple
from pathlib import Path

def is_sum_of_previous(num: int, prevs: List[int]) -> bool:
    seen = set()
    for prev in prevs:
        if num - prev in seen:
            return True
        seen.add(prev)
    return False

def find_first_invalid_number(numbers:List[int],*,preamble_len=25) -> int | None:
    for i in range(preamble_len, len(numbers)):
        if not is_sum_of_previous(numbers[i], numbers[i-preamble_len:i]):
            return numbers[i]
    return None

def find_contiguous_sum(number, numbers) -> List[int] | None:
    for i in range(0, len(numbers)):
        summ = numbers[i]
        j = i+1
        while summ < number:
            summ += numbers[j]
            if summ == number:
                return numbers[i:j+1]
            j +=1
    return None   


if __name__ == "__main__":
    with Path("inputs/day9.txt").open("r") as f:
        numbers = [int(line) for line in f]
    first = find_first_invalid_number(numbers)
    print(first)
    consecutives = find_contiguous_sum(first,numbers)
    mi = min(consecutives)
    mx = max(consecutives)
    print(mi+mx)
    