from enum import StrEnum, unique
from typing import Tuple, List
from dataclasses import dataclass
import math
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
@dataclass( slots=True)
class Action:
    action: ActionType
    value: int
    @classmethod
    def from_line(cls, line:str) ->"Action":
        line = line.rstrip()
        return cls(line[0], int(line[1:]))
class Ferry2:
    def __init__(self):
        self.waypoint_pos = [10,1]
        self.ship_pos = [0,0]
        self.current_heading: int = 0
        self.movements = {ActionType.NORTH: (0,1), ActionType.SOUTH: (0,-1), ActionType.EAST: (1,0), ActionType.WEST: (-1,0)}
    def __str__(self):
        return f"Ship: ({self.ship_pos[0]}, {self.ship_pos[1]})\nWaypoint: ({self.waypoint_pos[0]-self.ship_pos[0]}, {self.waypoint_pos[1] - self.ship_pos[1]})"
    def _update_waypoint_position(self, mov: Tuple[int, int],command):
            self.waypoint_pos = [m1 + (m2*command.value) for m1, m2 in zip(self.waypoint_pos, mov)]
    def move(self, command: Action) -> None:
        if command.action in self.movements.keys():
            mov: Tuple[int,int] = self.movements[command.action]
            self._update_waypoint_position(mov, command)
        elif command.action == ActionType.FORWARD:
            dist_x = self.waypoint_pos[0] - self.ship_pos[0]
            dist_y = self.waypoint_pos[1] - self.ship_pos[1]
            self.ship_pos[0] += dist_x*command.value
            self.ship_pos[1] += dist_y*command.value
            self.waypoint_pos[0] += dist_x*(command.value)
            self.waypoint_pos[1] += dist_y*(command.value)
        else:
            #calculate distance between ship and point:
            dx = self.waypoint_pos[0] - self.ship_pos[0]
            dy = self.waypoint_pos[1] - self.ship_pos[1]
            angle = command.value if command.action == ActionType.LEFT else -command.value
            theta = math.radians(angle)  # negating depends on rotation direction convention
            coss = math.cos(theta)
            sinn = math.sin(theta)
            rot_x = coss * dx - sinn * dy
            rot_y = sinn * dx + coss * dy
            self.waypoint_pos[0] = self.ship_pos[0] + rot_x
            self.waypoint_pos[1] = self.ship_pos[1] + rot_y
    def manhattan_distance(self) -> int:
        return sum(map(abs,self.ship_pos))

class Ferry:
    #__slots__ = ["current_pos","current_heading","direction_library","movements"]
    def __init__(self):
        self.waypoint_pos = [0,0]
        self.current_pos = [0,0]
        self.current_heading: int = 0
        self.direction_library = {0: (1,0), 90: (0,1), 180: (-1,0), 270: (0,-1)}
        self.movements = {ActionType.NORTH: (0,1), ActionType.SOUTH: (0,-1), ActionType.EAST: (1,0), ActionType.WEST: (-1,0)}
    def _update_position(self, mov: Tuple[int, int]):
            self.current_pos = [m1 + (m2*command.value) for m1, m2 in zip(self.current_pos, mov)]
    def move(self, command: Action) -> None:
        if command.action in self.movements.keys():
            mov: Tuple[int,int] = self.movements[command.action]
            self._update_position(mov)
        elif command.action == ActionType.FORWARD:
            mov: Tuple[int,int] = self.direction_library[self.current_heading]
            self._update_position(mov)
        else:
            self.current_heading += command.value if command.action==ActionType.LEFT else -command.value
            self.current_heading %= 360
    def manhattan_distance(self) -> int:
        return sum(map(abs,self.current_pos))
if __name__ == "__main__":
    commands: List[Action] = []
    ferry = Ferry()
    ferry2 = Ferry2()
    with open("inputs/day12.txt", "r") as file:
        commands = [Action.from_line(line) for line in file]
    for command in commands:
        ferry.move(command)
        ferry2.move(command)
    print(ferry.manhattan_distance())
    print(ferry2.manhattan_distance())


