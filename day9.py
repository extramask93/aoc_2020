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
#rework this to sliding window
def find_contiguous_sum_window(number, numbers) -> List[int] | None:
    window_start_idx = 0
    window_end_idx = 1
    window_sum = numbers[window_start_idx]
    while window_end_idx <= len(numbers):
        if window_sum < number and window_end_idx < len(numbers):
            window_sum += numbers[window_end_idx]
            window_end_idx +=1
            # extend right
        elif window_sum > number:
            window_sum -= numbers[window_start_idx]
            window_start_idx +=1
        elif window_sum == number and window_end_idx - window_start_idx > 1:
            return numbers[window_start_idx:window_end_idx]
        else:
            break
    return None


if __name__ == "__main__":
    with Path("inputs/day9.txt").open("r") as f:
        numbers = [int(line) for line in f]
    first = find_first_invalid_number(numbers)
    print(first)
    consecutives = find_contiguous_sum_window(first,numbers)
    mi = min(consecutives)
    mx = max(consecutives)
    print(mi+mx)
    