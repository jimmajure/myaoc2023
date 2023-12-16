from collections import Counter, defaultdict
from copy import copy
import itertools
import re


test_input = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""".split(
    "\n"
)

day11_input = open("day11_input.txt").read().split("\n")


class SpaceMap:
    def __init__(self, map, expansion_factor=1):
        self.map = map
        self.expansion_factor = expansion_factor
        new_rows = []
        for r in range(len(self.map)):
            if len(Counter(self.map[r])) == 1:
                new_rows.append(r)
        self.new_rows = new_rows

        new_cols = []
        for c in range(len(self.map[0])):
            if len(Counter([x[c] for x in self.map])) == 1:
                new_cols.append(c)
        self.new_cols = new_cols

        self.galaxies = []
        for r in range(len(self.map)):
            for c in range(len(self.map[r])):
                if self.map[r][c] == "#":
                    self.galaxies.append((r, c))

        self.galaxies = dict(zip(range(1, len(self.galaxies) + 1), self.galaxies))
        # adjust for expansion factor
        for g in self.galaxies:
            self.galaxies[g] = (
                self.galaxies[g][0]
                + self.expansion_factor
                * len([nr for nr in self.new_rows if nr < self.galaxies[g][0]])
                - len([nr for nr in self.new_rows if nr < self.galaxies[g][0]]),
                self.galaxies[g][1]
                + self.expansion_factor
                * len([nc for nc in self.new_cols if nc < self.galaxies[g][1]])
                - len([nc for nc in self.new_cols if nc < self.galaxies[g][1]]),
            )


if __name__ == "__main__":
    input = test_input
    input = day11_input

    input = [x for x in input if x]

    # print("---")
    # for line in input:
    #     print(line)

    # print("---")
    # for line in new_input:
    #     print(line)

    map = SpaceMap(input, 1000000)

    total = 0
    for combo in itertools.combinations(map.galaxies, 2):
        g1 = map.galaxies[combo[0]]
        g2 = map.galaxies[combo[1]]
        total += abs(g1[0]-g2[0]) + abs(g1[1]-g2[1])
        print(f"{combo[0]}/{combo[1]}: {abs(g1[0]-g2[0]) + abs(g1[1]-g2[1])}")

    print(total)