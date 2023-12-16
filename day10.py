from collections import defaultdict
from copy import copy
import re
from time import sleep
from typing import List, Tuple
from blessings import Terminal


test_input = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF""".split(
    "\n"
)

day10_input = open("day10_input.txt").read().split("\n")

test_input_2 = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""".split(
    "\n"
)

test_input_3 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
""".split(
    "\n"
)

test_input_4 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
""".split("\n")

moves = {
    "L": (0, -1),
    "R": (0, 1),
    "U": (-1, 0),
    "D": (1, 0),
}


class Map:
    def __init__(self, map: List[str]):
        self.map = map
        location = None
        for r in range(len(map)):
            for c in range(len(map[r])):
                if map[r][c] == "S":
                    location = (r, c)
                    break
            if location:
                break
        self.location = location
        self.start_location = location
        # replace S with an appropriate value
        self.map[location[0]] = (
            self.map[location[0]][: location[1]]
            + "F"
            + self.map[location[0]][location[1] + 1 :]
        )
        self.history = [location]
        self.direction_moved = None
        self.start()
        for r in range(len(self.map)):
            for c in range(len(self.map[r])):
                if (r, c) not in self.history and self.map[r][c] in "F7JL-|":
                    self.map[r] = (
                        self.map[r][: c]
                        + "o"
                        + self.map[r][c + 1 :]
                    )
        self.double_map()

    def double_map(self):
        self.map2 = []
        for r in range(len(self.map)):
            line = ""
            line2 = ""
            for c in range(len(self.map[r])):
                line += self.map[r][c]
                line2 += "|" if self.map[r][c] in "F7|" else "x"
                if c < len(self.map[r]) - 1:
                    line += "-" if self.map[r][c] in "LF-" else "x"
                    line2 += "x"

            self.map2.append(line)
            if r < len(self.map) - 1:
                self.map2.append(line2)

    def draw(self):
        print (t.clear())
        ln = 0
        for l in m.map2:
            with t.location(0,ln):
                print(l, end="", flush=True)
            ln += 1
        
    def area_enclosed(self):
        def location_from(loc, direction):
            return tuple([loc[i] + moves[direction][i] for i in range(2)])

        def can_get_out(loc, visited):
            # with t.location(loc[1], loc[0]):
            #     print(t.red+self.map2[loc[0]][loc[1]], end="", flush=True)
            # sleep(0.01)
            current_locaton = self.location
            self.location = loc
            dist_to_edge = sorted(
                [
                    ("U", loc[0]),
                    ("D", len(self.map2) - loc[0]),
                    ("L", loc[1]),
                    ("R", len(self.map2[0]) - loc[1]),
                ],
                key=lambda x: x[1],
            )
            visited.add(loc)
            try:
                for dir in dist_to_edge:
                    if location_from(loc, dir[0]) not in visited:
                        if self.peek2(dir[0]) is None:
                            return True
                        elif self.peek2(dir[0]) in "x.o":
                            if can_get_out(location_from(loc, dir[0]), visited):
                                return True
                return False
            finally:
                self.location = current_locaton
                # with t.location(loc[1], loc[0]):
                #     print(self.map2[loc[0]][loc[1]], end="", flush=True)

        area = 0
        total = 0
        visited = set()
        for r in range(len(self.map2)):
            for c in range(len(self.map2[r])):
                if self.map2[r][c] in "o.":
                    # self.draw()
                    total += 1
                    new_visited = set(visited)
                    if not can_get_out((r, c), new_visited):
                        visited = new_visited
                        print(f"Area enclosed at {r}, {c}")
                        area += 1

        return area, total

    def peek(self, direction: str):
        assert direction in ["U", "D", "L", "R"]
        at_loc = tuple([self.location[i] + moves[direction][i] for i in range(2)])
        if (
            at_loc[0] < 0
            or at_loc[1] < 0
            or at_loc[0] >= len(self.map)
            or at_loc[1] >= len(self.map[0])
        ):
            return None
        return self.map[at_loc[0]][at_loc[1]]

    def peek2(self, direction: str):
        assert direction in ["U", "D", "L", "R"]
        at_loc = tuple([self.location[i] + moves[direction][i] for i in range(2)])
        if (
            at_loc[0] < 0
            or at_loc[1] < 0
            or at_loc[0] >= len(self.map2)
            or at_loc[1] >= len(self.map2[0])
        ):
            return None
        return self.map2[at_loc[0]][at_loc[1]]

    def get_start_direction(self):
        if (v:=self.peek("U")) and v in "F7|":
            return "U"
        elif self.peek("D") in "JL|":
            return "D"
        elif self.peek("L") in "LF-":
            return "L"
        elif self.peek("R") in "7J-":
            return "R"
        else:
            return None

    def value(self):
        return self.map[self.location[0]][self.location[1]]

    def _do_move(self, direction: str):
        self.location = tuple(
            [self.location[i] + moves[direction][i] for i in range(2)]
        )
        self.direction_moved = direction
        self.history.append(self.location)

    def move(self):
        value = self.value()
        if value == "|":
            assert self.direction_moved in [
                "U",
                "D",
            ], f"Invalid direction for value {value}: {self.direction_moved}"
            direction = self.direction_moved
        elif value == "-":
            assert self.direction_moved in [
                "L",
                "R",
            ], f"Invalid direction for value {value}: {self.direction_moved}"
            direction = self.direction_moved
        elif value == "F":
            assert self.direction_moved in [
                "U",
                "L",
            ], f"Invalid direction for value {value}: {direction}"
            if self.direction_moved == "U":
                direction = "R"
            else:
                direction = "D"
        elif value == "7":
            assert self.direction_moved in [
                "U",
                "R",
            ], f"Invalid direction for value {value}: {direction}"
            if self.direction_moved == "U":
                direction = "L"
            else:
                direction = "D"
        elif value == "J":
            assert self.direction_moved in [
                "D",
                "R",
            ], f"Invalid direction for value {value}: {direction}"
            if self.direction_moved == "D":
                direction = "L"
            else:
                direction = "U"
        elif value == "L":
            assert self.direction_moved in [
                "D",
                "L",
            ], f"Invalid direction for value {value}: {direction}"
            if self.direction_moved == "D":
                direction = "R"
            else:
                direction = "U"

        self._do_move(direction)

    def start(self):
        # assert (
        #     self.map[self.location[0]][self.location[1]] == "S"
        # ), f"Invalid start location: {self.location}"
        start_direction = self.get_start_direction()
        self._do_move(start_direction)

        moves = 1
        while self.location != self.start_location:
            self.move()
            moves += 1

        return moves


if __name__ == "__main__":
    input = test_input
    input = day10_input
    # input = test_input_2
    # input = test_input_3
    # input = test_input_4

    input = [x for x in input if x]

    m = Map(input)
    print(m.start()/2)
    global t
    t = Terminal()
    with t.fullscreen():
        area = m.area_enclosed()
        pass
    print(f"Area enclosed: {area}")