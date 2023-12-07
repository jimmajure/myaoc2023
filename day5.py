from collections import defaultdict
import re


test_input = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
""".split(
    "\n"
)

day5_input = open("day5_input.txt").read().split("\n")
day5_input = [x for x in day5_input if x]


class Transformer:
    def __init__(self, name, definition, transformer=None):
        self.name = name
        self.definition = self._process_definition(definition)
        self.transformer = transformer

    def transform(self, value):
        in_value = value
        for definition in self.definition:
            if value in definition["source_range"]:
                value = definition["destination_start"] + (
                    value - definition["source_range"].start
                )
                break
        if self.transformer:
            value = self.transformer.transform(value)

        # print(f"{self.name} {in_value} {value}")
        return value

    def _process_definition(self, definition):
        result = []
        for line in definition:
            if line:
                data = [
                    int(g)
                    for g in re.fullmatch(r"(\d+)\s+(\d+)\s+(\d+)", line).groups()
                ]
                result.append(
                    {
                        "destination_start": data[0],
                        "source_range": range(data[1], data[1] + data[2]),
                        "length": data[2],
                    }
                )
        return result


def match_range(: List[range], range2: range): 

def is_within(range1: range, range2):
    if range1.start >= range2.start and range1.stop <= range2.stop:
        return True
    elif range1.start > range2.stop or range1.stop < range2.start:
        return False
    else:
        raise Exception("partial overlap")


class Transformer2:
    def __init__(self, name, definition, transformer=None):
        self.name = name
        self.definition = self._process_definition(definition)
        self.transformer = transformer

    def transform(self, value):
        in_value = value
        for definition in self.definition:
            if is_within(value, definition["source_range"]):
                new_start = definition["destination_start"] + (
                    value.start - definition["source_range"].start
                )
                value = range(new_start, new_start + len(value))
                break
        if self.transformer:
            value = self.transformer.transform(value)

        print(f"{self.name} {in_value} {value}")
        return value

    def _process_definition(self, definition):
        result = []
        for line in definition:
            if line:
                data = [
                    int(g)
                    for g in re.fullmatch(r"(\d+)\s+(\d+)\s+(\d+)", line).groups()
                ]
                result.append(
                    {
                        "destination_start": data[0],
                        "source_range": range(data[1], data[1] + data[2]),
                        "length": data[2],
                    }
                )
        return result


t1 = Transformer("t1", ["0 69 1", "1 0 69"])
assert t1.transform(-1) == -1, t1.transform(-1)
assert t1.transform(0) == 1, t1.transform(0)
assert t1.transform(1) == 2, t1.transform(1)
assert t1.transform(68) == 69, t1.transform(68)
assert t1.transform(69) == 0, t1.transform(69)
assert t1.transform(70) == 70, t1.transform(70)
assert t1.transform(71) == 71, t1.transform(71)

t2 = Transformer2("t2", ["0 69 5", "1 0 69"])
assert t2.transform([range(1,5)]) == [range(2,6)]

if __name__ == "__main__":
    input = test_input
    # input = day5_input

    total = 0
    seeds = [int(sn) for sn in re.split(r"\s+", input.pop(0).split(":")[1].strip())]
    seeds2 = [(seeds[i * 2], seeds[i * 2 + 1]) for i in range(int(len(seeds) / 2))]
    seeds = []
    for seed_spec in seeds2:
        seeds.append( range(seed_spec[0], seed_spec[0] + seed_spec[1]))
    print(seeds)

    transformer_base = None
    transformer = None
    transformer_def = []
    while not (line := input.pop(0)).endswith("map:"):
        pass

    while len(input) > 0:
        name = line[:-1]
        transformer_def = []
        while len(input) > 0 and not (line := input.pop(0)).endswith("map:"):
            transformer_def.append(line)
        next_transformer = Transformer2(name, transformer_def)
        if not transformer_base:
            transformer_base = next_transformer
        if transformer:
            transformer.transformer = next_transformer
        transformer = next_transformer

    min_value = 100000000000000000000000
    for seed in seeds:
        # print("\n\nseed", seed)
        # print(transformer_base.transform(seed))
        min_value = min(min_value, transformer_base.transform(seed).start)

    print("min", min_value)
