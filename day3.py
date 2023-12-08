from collections import defaultdict
import re
from functools import reduce
from string import digits
from typing import List


test_input = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""".split(
    "\n"
)

day3_input = open("day3_input.txt").read().split("\n")
day3_input = [l for l in day3_input if l]

def get_symbols(schematic) -> str:
    sc_set = set()
    for l in schematic:
        sc_set = sc_set.union(set([c for c in l]))
    return [c for c in sc_set if c not in (digits + ".")]


assert set(get_symbols(test_input)) == set(["*", "#", "+", "$"]), get_symbols(
    test_input
)

class Schematic:

    def __init__(self, data: List[str]) -> None:
        self._raw = data
        self._length = len(self._raw)
        self.symbols = get_symbols(data)
        self.parts = defaultdict(list)
        self._process_raw_schematic()

    def get_part_numbers(self):
        result = []
        for pn_list in self.parts.values():
            result += pn_list
        return result
    
    def get_gears_ratios(self):
        result = []
        for symbol in self.parts:
            if symbol[2] == "*":
                part = self.parts[symbol]
                if len(part) == 2:
                    result.append(part[0]*part[1])

        return result

    def _process_raw_schematic(self):
        for row in range(len(self._raw)):
            schematic_row = str(self._raw[row])
            for part_no, start, end in Schematic.part_number_generator(schematic_row):
                lines = [ln for ln in range(row - 1, row + 2) if self._length > ln >= 0]
                for line in lines:
                    for pos in [pos for pos in range(start-1, end+1) if len(self._raw[line]) > pos >= 0]:
                        if self._raw[line][pos] in self.symbols:
                            self.parts[(line, pos, self._raw[line][pos])].append(part_no)

    def part_number_generator(schematic_row):
        for m in re.finditer(r"([0-9]+)", schematic_row):
            yield int(m.group(1)), m.start(), m.end()


if __name__ == "__main__":
    part_numbers = []
    raw = test_input
    raw = day3_input

    schematic = Schematic(raw)
    print(schematic.get_part_numbers())
    print(sum(schematic.get_part_numbers()))

    print(schematic.get_gears_ratios())
    print(sum(schematic.get_gears_ratios()))