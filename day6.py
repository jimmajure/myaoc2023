from collections import defaultdict
import re


test_input = """Time:      7  15   30
Distance:  9  40  200""".split(
    "\n"
)

# day6_input = open("day6_input.txt").read().split("\n")
# day6_input = [x for x in day6_input if x]

def run_race(time_to_hold, duration):
    return time_to_hold * (duration - time_to_hold)


if __name__ == "__main__":
    input = [(7,9), (15 ,40), (30, 200)]
    test_input_2 = [(71530, 940200)]
    input = test_input_2
    day6_input = [(45, 305), (97, 1062), (72, 1110), (95, 1695)]
    # input = day6_input
    day6_input_2 = [(45977295, 305106211101695)]
    input = day6_input_2

    value = 1
    for race in input:
        winners = 0
        duration, record = race
        for i in range(duration+1):
            distance = run_race(i, duration)
            # print(f"{i}: {(distance :=run_race(i, duration))}")
            if distance > record:
                winners += 1
        value *= winners
    print(f"Winners: {value}")


