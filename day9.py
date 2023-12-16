from collections import defaultdict
from copy import copy
import re


test_input = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""".split(
    "\n"
)

day9_input = open("day9_input.txt").read().split("\n")

if __name__ == "__main__":
    input = test_input
    input = day9_input

    input = [x for x in input if x]

    total_new_values = 0
    for line in input:
        seq = [int(x) for x in line.split()]
        print(seq)
        sequences = [seq]
        while not len(set(seq)) == 1:
            seq = [seq[i] - seq[i - 1] for i in range(1, len(seq))]
            sequences.append(seq)
    
        # for idx in range(len(sequences)-1, 0, -1):
        #     sequences[idx-1].append(sequences[idx-1][-1]+sequences[idx][-1])

        for idx in range(len(sequences)-1, 0, -1):
            sequences[idx-1] = [(sequences[idx-1][0])-(sequences[idx][0])] + sequences[idx-1]

        print(sequences[0])
        total_new_values += sequences[0][0]
    print(total_new_values)
