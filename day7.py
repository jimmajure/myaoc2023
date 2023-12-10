from collections import Counter, defaultdict
import re


test_input = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""".split(
    "\n"
)

day7_input = open("day7_input.txt").read().split("\n")
day7_input = [x for x in day7_input if x]

hand_types = {
    1: "Five of a kind",
    2: "Four of a kind",
    3: "Full house",
    4: "Three of a kind",
    5: "Two pair",
    6: "One pair",
    7: "Nothing",
}

card_rank = "AKQT98765432J"


class Hand:
    def __init__(self, cards: str, wildcard: str = "J"):
        self.cards = cards
        assert (
            not wildcard or len(wildcard) == 1
        ), f"Wildcard must be a single character: {wildcard}"
        self.wildcard = wildcard
        self.type = self._get_type()

    def _get_type(self):
        counter = Counter(self._eval_wildcard())
        if len(counter) == 1:
            return 1
        elif len(counter) == 2:
            if 4 in counter.values():
                return 2
            elif 3 in counter.values():
                return 3
        elif len(counter) == 3:
            if 3 in counter.values():
                return 4
            elif 2 in counter.values():
                return 5
        elif len(counter) == 4:
            return 6
        elif len(counter) == 5:
            return 7

    def compare_card(card1, card2):
        return card_rank.index(card1) - card_rank.index(card2)

    def _eval_wildcard(self):
        counter = Counter(self.cards)
        alt = self.cards
        not_wildcard = [x for x in counter.keys() if x != self.wildcard]
        if len(not_wildcard) == len(counter):
            # no wildcards
            return alt

        highest_not_wildcard = not_wildcard[0] if not_wildcard else None
        for card in not_wildcard:
            if Hand.compare_card(card, highest_not_wildcard) < 0:
                highest_not_wildcard = card

        if len(counter) == 1:
            # they are all jokers
            assert (
                len(not_wildcard) == 0 and alt[0] == self.wildcard
            ), f"Wildcard is not a joker: {self.wildcard}"
            alt = alt.replace(self.wildcard, card_rank[0])
        elif len(counter) == 2 and self.wildcard in counter.keys():
            assert len(not_wildcard) == 1, f"More than one non-wildcard: {not_wildcard}"
            # there are jokers and one other card, make it the same as the other card
            alt = alt.replace(self.wildcard, not_wildcard[0])
        elif len(counter) == 3 and self.wildcard in counter.keys():
            assert len(not_wildcard) == 2, f"More than 2 non-wildcard: {not_wildcard}"
            if counter[not_wildcard[0]] == counter[not_wildcard[1]]:
                # there are two pairs or 3 jokers
                # replace the wildcard with the higher card
                alt = alt.replace(self.wildcard, highest_not_wildcard)
            elif counter[not_wildcard[0]] == 2:
                # there is a pair and 2 jokers, make it the same as the pair
                alt = alt.replace(self.wildcard, not_wildcard[0])
            elif counter[not_wildcard[1]] == 2:
                # there is a pair and 2 jokers, make it the same as the pair
                alt = alt.replace(self.wildcard, not_wildcard[1])
            elif counter[not_wildcard[0]] == 3:
                alt = alt.replace(self.wildcard, not_wildcard[0])
            else:
                alt = alt.replace(self.wildcard, not_wildcard[1])
        elif len(counter) == 4:
            # there is a pair and 1 joker, make it the same as the pair
            # or 2 jokers and three cards
            pair_card = [x for x in counter.keys() if counter[x] == 2][0]
            if pair_card == self.wildcard:
                alt = alt.replace(self.wildcard, highest_not_wildcard)
            else:
                alt = alt.replace(self.wildcard, pair_card)
        elif len(counter) == 5:
            # there is 1 joker, make it the highest card
            assert len(not_wildcard) == 4, f"More than 4 non-wildcard: {not_wildcard}"
            alt = alt.replace(self.wildcard, highest_not_wildcard)
        else:
            raise Exception(f"Invalid hand: {self.cards}")
        return alt

    def __repr__(self):
        return f"{hand_types[self.type]}: {self.cards}"

    def __str__(self):
        return f"{self.name}: {self.cards}"

    def __gt__(self, other):
        return Hand.__compare__(self, other) == -1

    def __lt__(self, other):
        return Hand.__compare__(self, other) == 1

    def __eq__(self, other):
        return Hand.__compare__(self, other) == 0

    def __ne__(self, other):
        return self.cards != other.cards

    def __ge__(self, other):
        return Hand.__compare__(self, other) in (-1, 0)

    def __le__(self, other):
        return Hand.__compare__(self, other) in (1, 0)

    def __hash__(self):
        return hash(self.cards)

    def __compare__(hand1, hand2):
        result = None
        if hand1.type < hand2.type:
            result = -1
        elif hand1.type > hand2.type:
            result = 1
        else:
            for idx in range(len(hand1.cards)):
                if card_rank.index(hand1.cards[idx]) < card_rank.index(
                    hand2.cards[idx]
                ):
                    result = -1
                    break
                elif card_rank.index(hand1.cards[idx]) > card_rank.index(
                    hand2.cards[idx]
                ):
                    result = 1
                    break
            result = 0 if result is None else result

        if result == 0:
            print (f"Equal: {hand1} {hand2}")
        return result


h1 = Hand("88885")
h2 = Hand("T55J5")

assert h1.type == h2.type
assert h1 < h2


h1 = Hand("22222")
assert h1.type == 1

h2 = Hand("JJJJJ")
assert h2.type == 1

assert h1 > h2
assert h2 < h1
assert h1 >= h2
assert h2 <= h1


h1 = Hand("QQJJ2")
assert h1.type == 2

h1 = Hand("JJ789")
assert h1.type == 4

h1 = Hand("QJ222")
assert h1.type == 2

h1 = Hand("QJJJ2")
assert h1.type == 2

h1 = Hand("QQJ22")
assert h1.type == 3

h1 = Hand("QQQ22")
assert h1.type == 3

h1 = Hand("QJ522")
assert h1.type == 4

h1 = Hand("Q2522")
assert h1.type == 4

h1 = Hand("QQ522")
assert h1.type == 5

h1 = Hand("QJ57K")
assert h1.type == 6, h1.type

h1 = Hand("23456")
assert h1.type == 7, h1.type

h1 = Hand("AA7K2")
h2 = Hand("2Q35Q")

assert h1 > h2
print(sorted([h1, h2]))

if __name__ == "__main__":
    input = test_input
    input = day7_input
    hands = []
    for line in input:
        m = re.fullmatch(r"([A-Z0-9]{5})\s+(\d+)", line)
        hand = Hand(m.group(1))
        hands.append((hand, int(m.group(2))))

    hands.sort(key=lambda x: x[0])
    ranked = list(zip(range(1, len(hands) + 1), hands))
    for hand in ranked:
        print(hand, (hand[0] * hand[1][1]))
        pass

    value = 0
    for hand in ranked:
        value += hand[0] * hand[1][1]

    print(f"Value: {value}")
# 248820779
