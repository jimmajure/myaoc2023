
import re


test_input = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""".split("\n")

test_input2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""".split("\n")

valid_digits = [d for d in "123456789"]
valid_digits += ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
digit_values = dict(zip(valid_digits, [int(d) for d in "123456789"]*2))
print(digit_values)
token_re = "|".join([f"({dg})" for dg in valid_digits])

def pull_digits(line):
    digits = []
    while (m := re.search(token_re, line)) is not None:
        digits.append(m.group(0))
        line = line[m.start()+1:]
    return [digit_values[d] for d in digits]

if __name__ == "__main__":

    input = test_input
    input = test_input2
    input = open("day1_input.txt", "r").read().split("\n")
    input = [l for l in input if l]

    total_calibration = 0
    for line in input:
        digits = pull_digits(line)
        print(digits)
        assert len(digits) > 0

        total_calibration += int(digits[0])*10+int(digits[-1])

    print(f"Total calibrarion: {total_calibration}")
