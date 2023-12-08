import re
from functools import reduce


test_input = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""".split(
    "\n"
)


def get_game(game: str):
    return int(game[5 : (colon := game.index(":"))]), game[colon + 1 :].strip()


assert get_game(test_input[0]) == (
    1,
    "3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
), get_game(test_input[0])

if __name__ == "__main__":
    bag = {
        "red": 12,
        "blue": 14,
        "green": 13,
    }
    input = test_input

    input = open("day2_input.txt", "r").read().split("\n")
    input = [l for l in input if l]

    id_sum = 0
    for game in input:
        game_possible = True
        game_number, rest = get_game(game)
        for draw in rest.split(";"):
            for color in draw.split(","):
                m = re.fullmatch(r"([0-9]+) (red|green|blue)", color.strip())
                if int(m.group(1)) > bag[m.group(2)]:
                    game_possible = False
                    break
            if not game_possible:
                break
        if game_possible:
            id_sum += game_number

    print(f"ID Sum: {id_sum}")

    total_power = 0
    for game in input:
        color_mins = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }
        game_number, rest = get_game(game)
        for draw in rest.split(";"):
            for color in draw.split(","):
                m = re.fullmatch(r"([0-9]+) (red|green|blue)", color.strip())
                color_mins[m.group(2)] = max(color_mins[m.group(2)], int(m.group(1)))
        game_power = reduce((lambda x, y: x * y),color_mins.values())
        print(f"Game power: {game_power}")
        total_power += game_power

    print(f"Total Power: {total_power}")
