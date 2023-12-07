from collections import defaultdict
import re


test_input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""".split(
    "\n"
)

day4_input = open("day4_input.txt").read().split("\n")
day4_input = [x for x in day4_input if x]

if __name__ == "__main__":
    input = test_input
    input = day4_input

    total = 0
    for line in input:
        winning_numbers, my_numbers = line.split(":", maxsplit=1)[1].split("|")
        winning_numbers = [int(x) for x in winning_numbers.split(" ") if x]
        my_numbers = [int(x) for x in my_numbers.split(" ") if x]

        my_winners = set(winning_numbers) & set(my_numbers)
        if my_winners:
            total += 2 ** (len(set(winning_numbers) & set(my_numbers)) - 1)

    print(total)

    cards = {i: 1 for i in range(1, len(input)+1)}
    total = 0
    for line in input:
        card_number = int(re.fullmatch(r"Card\s+(\d+)",line.split(":", maxsplit=1)[0]).group(1))
        winning_numbers, my_numbers = line.split(":", maxsplit=1)[1].split("|")
        winning_numbers = [int(x) for x in winning_numbers.split(" ") if x]
        my_numbers = [int(x) for x in my_numbers.split(" ") if x]

        my_winners = set(winning_numbers) & set(my_numbers)
        for i in range(card_number + 1, card_number+len(my_winners) + 1):
            cards[i] += cards[card_number]

    print(sum(cards.values()))
