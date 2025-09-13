from pathlib import Path
from typing import NamedTuple, Callable, Any
from dataclasses import dataclass
@dataclass(frozen=True)
class Policy:
    min: int
    max: int
    letter: str
    password: str
    def validate_policy_1(self) -> bool:
        return self.min <= self.password.count(self.letter) <= self.max
    def validate_policy_2(self) -> bool:
        return (self.password[self.min-1] == self.letter) ^ (self.password[self.max-1] == self.letter)
def parse_policy(line: str) -> Policy:
    min_max, letter, password = line.strip().split()
    min, max = map(int, min_max.split("-"))
    letter = letter.rstrip(":")
    return Policy(min,max,letter,password)

def load_input(path: Path, parser: Callable[[str], Any]) -> Any:
    with path.open("r") as file:
        for line in file:
            yield parser(line)

if __name__ == "__main__":
    valid_cnt_part1 = 0
    valid_cnt_part2 = 0
    for policy in load_input(Path("inputs") / "day2.txt", parse_policy):
        if policy.validate_policy_1():
            valid_cnt_part1 +=1
        if policy.validate_policy_2():
            valid_cnt_part2 +=1
    print(f"Part1: {valid_cnt_part1}")
    print(f"Part2: {valid_cnt_part2}")
