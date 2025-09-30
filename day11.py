from enum import StrEnum
from typing import List, Tuple
from functools import cache, partialmethod
import copy

class SeatType(StrEnum):
    floor = "."
    empty = "L"
    occupied  = "#"

class FloorPlan():
    __slots__ = ["seat_map", "max_x", "max_y", "pos_generator"]
    def __init__(self, seat_map, pos_generator=None):
        self.seat_map = seat_map
        self.max_x = len(seat_map[0])
        self.max_y = len(seat_map)
        if pos_generator is None:
            self.pos_generator = self.positions_cache
    def get_occupied_seats(self):
        return sum(row.count(SeatType.occupied) for row in self.seat_map)
    def __str__(self):
        result = []
        for row in range(len(self.seat_map)):
            for col in range(len(self.seat_map[0])):
                result.append(str(self.seat_map[row][col]))
            result.append("\n")
        return "".join(result)
    @cache
    def positions_cache_part2(self, x:int, y:int):
        moves = [(-1,-1), (0,-1), (1,-1), (1,0),(1,1),(0,1), (-1,1), (-1,0)]
        positions = []
        for mov in moves:
            temp_x = x
            temp_y = y
            while True:
                #on the edge, so stop
                if temp_x+mov[0] < 0 or  temp_y+mov[1] < 0 or temp_x+mov[0]>=self.max_x or temp_y+mov[1]>=self.max_y:
                    break
                elif self.seat_map[temp_y+mov[1]][temp_x+mov[0]] == SeatType.floor:
                    temp_x += mov[0]
                    temp_y += mov[1]
                    continue
                else:
                    positions.append((temp_x+mov[0], temp_y+mov[1]))
                    break
        return positions
        
    @cache
    def positions_cache(self, x: int, y:int) -> List[Tuple[int,int]]:
        pos_list = [(-1,-1), (0,-1), (1,-1), (1,0),(1,1),(0,1), (-1,1), (-1,0)]
        def filter_pos(pos):
            return not(x+pos[0] < 0 or  y+pos[1] < 0 or x+pos[0]>=self.max_x or y+pos[1]>=self.max_y)
        new_pos = lambda pos: (x+pos[0], y+pos[1])
        return list(map(new_pos,filter(filter_pos, pos_list)))
                
    def get_neighbours(self, x:int,y:int):
        return [self.seat_map[pos[1]][pos[0]] for pos in self.pos_generator(x,y)]
    def simulate(self, empty_treshold = 4):
        has_changed = False
        new_seat_map = copy.deepcopy(self.seat_map)
        for y in range(len(self.seat_map)):
            for x in range(len(self.seat_map[0])):
                if self.seat_map[y][x] == SeatType.floor:
                    continue
                occupied_count = self.get_neighbours(x,y).count(SeatType.occupied)
                if self.seat_map[y][x] == SeatType.empty and occupied_count == 0:
                    new_seat_map[y][x] = SeatType.occupied
                    has_changed = True
                elif self.seat_map[y][x] == SeatType.occupied and occupied_count >=empty_treshold:
                    new_seat_map[y][x] = SeatType.empty
                    has_changed = True
        if has_changed:
            self.seat_map =new_seat_map
        return has_changed




if __name__ == "__main__":
    seats: List[List[SeatType]] = []
    with open("inputs/day11.txt","r") as file:
        for line in file:
            row = []
            for c in line.strip():
                row.append(SeatType(c))
            seats.append(row)
    floor_plan = FloorPlan(seats)
    treshold = 5
    floor_plan.pos_generator = floor_plan.positions_cache_part2
    time = 0
    res = True
    while res:
        time+=1
        res = floor_plan.simulate(empty_treshold=treshold)
    
    print(floor_plan.get_occupied_seats())

    

