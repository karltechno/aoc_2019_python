def solve_day1_part2(input):
    fuel = 0
    for x in input:
        while x > 0:
            x = int(x / 3) - 2
            fuel += max(0, x)
    
    return fuel

def solve_day1(input):
    return sum([int(x / 3) - 2 for x in input])

if __name__ == "__main__":
    with open("inputs/day1.txt") as f:
        day1_input = [int(x) for x in f.readlines()]
        part1 = solve_day1(day1_input)
        part2 = solve_day1_part2(day1_input)
        print(f"part1 : {part1}")
        print(f"part2 : {part2}")
