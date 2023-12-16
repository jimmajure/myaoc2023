from collections import defaultdict
from copy import copy
import re


test_input = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""".split(
    "\n"
)

test_input_2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""".split(
    "\n"
)

test_input_3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""".split(
    "\n"
)

day8_input = open("day8_input.txt").read().split("\n")


def run_race(time_to_hold, duration):
    return time_to_hold * (duration - time_to_hold)


if __name__ == "__main__":
    input = copy(test_input)
    input = copy(test_input_3)
    input = day8_input
    instructions = input.pop(0)

    input = [x for x in input if x]
    nodes = {}
    for line in input:
        m = re.fullmatch(r"([A-Z0-9]{3})\s+=\s+\(([A-Z0-9]{3}), ([A-Z0-9]{3})\)", line)
        nodes[m.group(1)] = (m.group(2), m.group(3))

    instruction_map = {"R": 1, "L": 0}

    current_nodes = [n for n in nodes if n.endswith("A")]
    print(f"Starting nodes: {current_nodes}")
    print(f"Z nodes: {[cn for cn in nodes if cn.endswith('Z')]}")

    def get_instruction():
        if (next_instruction := next(get_instruction.itera, None)) is None:
            get_instruction.itera = iter(instructions)
            next_instruction = next(get_instruction.itera, None)
        return next_instruction

    get_instruction.itera = iter(instructions)

    steps = 0
    while not all(cn.endswith("Z") for cn in current_nodes):
        if steps % len(instructions) == 0:
            print(f"Current nodes: {current_nodes}")
        inst_idx = instruction_map[get_instruction()]

        next_nodes = [nodes[cn][inst_idx] for cn in current_nodes]

        current_nodes = next_nodes
        steps += 1
        if steps % 1000000 == 0:
            print(f"Steps: {steps}")

    print(f"Steps: {steps}")
