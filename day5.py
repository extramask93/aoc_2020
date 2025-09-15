from pathlib import Path
from typing import Set, Iterator
from dataclasses import dataclass
import itertools


@dataclass(frozen=True)
class Seat():
    row:int
    col:int
    seat_id: int
    @classmethod
    def from_chars(cls, s: str) -> "Seat":
        rows = range(128)
        cols = range(8)
        for c in s[0:7]:
            midpoint = len(rows) // 2
            if c == "F":
                rows = rows[:midpoint]
            elif c == "B":
                rows = rows[midpoint:]
            else:
                raise RuntimeError()
        for c in s[7:]:
            midpoint = len(cols) // 2
            if c == "R":
                cols = cols[midpoint:]
            elif c == "L":
                cols = cols[:midpoint]
            else:
                raise RuntimeError()
        return cls(rows[0], cols[0], rows[0]*8 + cols[0])

def load_input(path: Path)->Iterator[str]:
    with path.open("r") as file:
        for line in file:
            yield line.strip()
if __name__ == "__main__":
    seats = [Seat.from_chars(line) for line in load_input(Path("inputs/day5.txt"))]
    found_seats: Set[Seat] =set(seats)
    seats_ids = [seat.seat_id for seat in seats]
    all_seats = {Seat(r,c,r*8+c) for c,r in itertools.product(range(8),range(128))}
    missing_seats = all_seats.difference(found_seats)
    places = [missing_seat for missing_seat in missing_seats if 0<missing_seat.col<8]
    places = [place for place in places if (place.seat_id+1 in seats_ids and place.seat_id-1 in seats_ids)]
    max_id = max(seats_ids)
    print(max_id)
    print(places)