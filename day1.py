from pathlib import Path

def read_input_values(path: Path) -> str:
    with path.open("r") as file:
        for line in file:
            yield line.strip()
        


if __name__ == "__main__":
    values = (int(x) for x in read_input_values(Path("inputs") / "day1.txt"))
    seen = set()
    for val in values:
        complement = 2020-val
        if complement in seen:
            print(complement*val)
            break
        seen.add(val)