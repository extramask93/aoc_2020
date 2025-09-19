from pathlib import Path
from typing import List, Set, Iterator, Tuple, FrozenSet
from dataclasses import dataclass
@dataclass
class Group:
    responses: Tuple[FrozenSet[str], ...]
    @classmethod
    def from_lines(cls, arr: List[str])->"Group":
        all_responses: List[FrozenSet[str]] = []
        for answers in arr:
            responses = answers.strip()
            if responses:
                all_responses.append(frozenset(responses))
        return cls(tuple(all_responses))
    def any_yes_responses(self)->FrozenSet[str]:
        return frozenset.union(*self.responses)
    def all_yes_responses(self)->FrozenSet[str]:
        return frozenset.intersection(*self.responses)



def load_input(path: Path)->Iterator[List[str]]:
    with path.open("r") as file:
        group: List[str] = []
        for line in file:
            if not line.strip():
                yield group
                group = []
            group.append(line)
        yield group

if __name__ == "__main__":
    groups = [Group.from_lines(group) for group in load_input(Path("inputs") / "day6.txt")]
    print(sum(len(group.any_yes_responses()) for group in groups))
    print(sum(len(group.all_yes_responses()) for group in groups))