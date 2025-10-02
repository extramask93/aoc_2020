from enum import StrEnum, unique
from dataclasses import dataclass
input = """F10
N3
F7
R90
F11"""
@unique
class ActionType(StrEnum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"
    RIGHT = "R"
    LEFT = "L"
    FORWARD= "F"
@dataclass(frozen=True, slots=True)
class Action:
    action: ActionType
    value: int

class Ferry:
    __slots__ = ["current_pos","current_heading","direction_library","movements"]
    def __init__(self):
        self.current_pos = [0,0]
        self.current_heading: int = 0
        self.direction_library = {0: (1,0), 90: (0,1), -90: (0,-1), 180: (-1,0), -180:(-1,0),  270: (0,-1), -270: (0,1)}
        self.movements = {ActionType.NORTH: (0,1), ActionType.SOUTH: (0,-1), ActionType.EAST: (1,0), ActionType.WEST: (-1,0)}
    def move(self, command):
        if command.action in [ActionType.NORTH, ActionType.EAST, ActionType.SOUTH, ActionType.WEST]:
            mov = self.movements[command.action]
            self.current_pos = [m1 + (m2*command.value) for m1, m2 in zip(self.current_pos, mov)]
        elif command.action == ActionType.FORWARD:
            mov = self.direction_library[self.current_heading]
            self.current_pos = [m1 + (m2*command.value) for m1, m2 in zip(self.current_pos, mov)]
        else:
            self.current_heading += command.value if command.action==ActionType.LEFT else -command.value
            self.current_heading %= 360
    def manhattan_distance(self):
        return sum(map(abs,self.current_pos))
if __name__ == "__main__":
    commands = []
    ferry = Ferry()
    with open("inputs/day12.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            action = ActionType(line[0])
            value = int(line[1:])
            commands.append(Action(action,value))
    for command in commands:
        ferry.move(command)
        print(ferry.current_pos)
    print(ferry.manhattan_distance())


