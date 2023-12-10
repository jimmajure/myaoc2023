from collections import defaultdict
import re
from typing import List


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


class RangeList:
    def __init__(self, range_list: List[range]) -> None:
        self.range_list = sorted(range_list, key=lambda x: x.start)
        self.range_list = self._merge(self.range_list)
        # assert all(x.stop <= y.start for x, y in zip(self.range_list, self.range_list[1:]))

    def _merge(self, range_list: List[range]) -> List[range]:
        new_range_list = []
        for rng in range_list:
            if new_range_list and rng.start < new_range_list[-1].stop:
                new_range_list[-1] = range(new_range_list[-1].start, rng.stop)
            else:
                new_range_list.append(rng)
        return new_range_list
    
    def __repr__(self) -> str:
        return f"RangeList({self.range_list})"

    def align(self, range_list: "RangeList") -> "RangeList":
        outiter = iter(range_list.range_list)
        myiter = iter(self.range_list)

        myrange = next(myiter)
        outrange = next(outiter)
        new_range_list = []
        while outrange and myrange:
            if outrange.stop <= myrange.start:
                # before myrange
                new_range_list.append(outrange)
                outrange = next(outiter, None)
            elif outrange.start < myrange.start and outrange.stop <= myrange.stop:
                new_range_list.append(range(outrange.start, myrange.start))
                new_range_list.append(range(myrange.start, outrange.stop))
                outrange = next(outiter, None)
            elif outrange.start >= myrange.start and outrange.stop <= myrange.stop:
                # contained in myrange
                new_range_list.append(outrange)
                outrange = next(outiter, None)
            elif (
                myrange.start <= outrange.start < myrange.stop
                and outrange.stop > myrange.stop
            ):
                new_range_list.append(range(outrange.start, myrange.stop))
                outrange = range(myrange.stop, outrange.stop)
                myrange = next(myiter, None)
            elif outrange.start >= myrange.stop:
                myrange = next(myiter, None)
        if not myrange:
            new_range_list.append(outrange)
            for outrange in outiter:
                new_range_list.append(outrange)
        return RangeList(new_range_list)


rl1 = RangeList([range(3, 10)])
rl2 = RangeList([range(4, 7)])
assert rl1.align(rl2).range_list == [range(4, 7)], rl1.align(rl2).range_list
assert rl1.align(RangeList([range(1, 2)])).range_list == [range(1, 2)]
assert rl1.align(RangeList([range(1, 3)])).range_list == [
    range(1, 3),
], rl1.align(RangeList([range(1, 3)])).range_list
assert (out := rl1.align(RangeList([range(1, 7)])).range_list) == [
    range(1, 3),
    range(3, 7),
], out
assert (out := rl1.align(RangeList([range(10, 12)])).range_list) == [range(10, 12)], out
rl1 = RangeList([range(10, 20), range(30, 40)])
rl2 = RangeList([range(0, 5), range(21, 30), range(40, 45)])
assert rl1.align(rl2).range_list == rl2.range_list, rl1.align(rl2).range_list
assert (out := rl1.align(RangeList([range(17, 33)])).range_list) == [
    range(17, 20),
    range(20, 30),
    range(30, 33),
], out
assert (out := rl1.align(RangeList([range(5, 11), range(17, 33)])).range_list) == [
    range(5, 10),
    range(10, 11),
    range(17, 20),
    range(20, 30),
    range(30, 33),
], out
rl1 = RangeList([range(45, 64), range(64, 77), range(77, 100)])
rl2 = RangeList([range(74, 88)])
assert (out := rl1.align(rl2).range_list) == [range(74, 77), range(77, 88)], out



def is_within(range1: range, range2):
    if range1.start >= range2.start and range1.stop <= range2.stop:
        return True
    elif range1.start >= range2.stop or range1.stop <= range2.start:
        return False
    else:
        raise Exception(f"partial overlap: {range1} {range2}")


class Transformer:
    def __init__(self, name, definition, transformer=None):
        self.name = name
        self.definition = self._process_definition(definition)
        self.transformer = transformer

    def transform(self, value: RangeList):
        in_value = value
        tran_range_list = RangeList([v["source_range"] for v in self.definition])
        value = tran_range_list.align(value)
        new_value = []
        for rng in value.range_list:
            for definition in self.definition:
                try:
                    if is_within(rng, definition["source_range"]):
                        new_start = definition["destination_start"] + (
                            rng.start - definition["source_range"].start
                        )
                        new_value.append(range(new_start, new_start + len(rng)))
                except Exception as e:
                    print(tran_range_list)
                    print(in_value)
                    exit(0)
            if not new_value:
                new_value += value.range_list
        value = RangeList(new_value)
        if self.transformer:
            value = self.transformer.transform(value)

        print(f"{self.name} {in_value} {value}")
        return value

    # Exception: partial overlap: range(722763618, 748123067) range(689055790, 747670686)
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


# t1 = Transformer("t1", ["0 69 1", "1 0 69"])
# assert t1.transform(-1) == -1, t1.transform(-1)
# assert t1.transform(0) == 1, t1.transform(0)
# assert t1.transform(1) == 2, t1.transform(1)
# assert t1.transform(68) == 69, t1.transform(68)
# assert t1.transform(69) == 0, t1.transform(69)
# assert t1.transform(70) == 70, t1.transform(70)
# assert t1.transform(71) == 71, t1.transform(71)

t2 = Transformer("t2", ["0 69 5", "1 0 69"])
assert (out := t2.transform(RangeList([range(1, 5)])).range_list) == [range(2, 6)], out

if __name__ == "__main__":
    input = test_input
    input = day5_input

    total = 0
    seeds = [int(sn) for sn in re.split(r"\s+", input.pop(0).split(":")[1].strip())]
    seeds2 = [(seeds[i * 2], seeds[i * 2 + 1]) for i in range(int(len(seeds) / 2))]
    seeds = []
    for seed_spec in seeds2:
        seeds.append(range(seed_spec[0], seed_spec[0] + seed_spec[1]))
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
        next_transformer = Transformer(name, transformer_def)
        if not transformer_base:
            transformer_base = next_transformer
        if transformer:
            transformer.transformer = next_transformer
        transformer = next_transformer

    min_value = 100000000000000000000000
    for seed in seeds:
        # print("\n\nseed", seed)
        # print(transformer_base.transform(seed))
        min_value = min(
            min_value, transformer_base.transform(RangeList([seed])).range_list[0].start
        )

    print("min", min_value)
