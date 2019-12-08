def sign_zero(x):
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1

def build_occupancy_dict(lines):
    step_dict = dict()
    step_dict['U'] = lambda x, v : (x[0], x[1] + v)
    step_dict['D'] = lambda x, v : (x[0], x[1] - v)
    step_dict['L'] = lambda x, v : (x[0] - v, x[1])
    step_dict['R'] = lambda x, v : (x[0] + v, x[1])

    pos = (0, 0)
    occupancy = dict()

    steps = 0

    for line in lines:
        new_pos = step_dict[line[0]](pos, line[1])
        delta = tuple(map(lambda x, y : sign_zero(y - x), pos, new_pos))

        while pos != new_pos:
            pos = tuple(map(lambda x, y : x + y, pos, delta))
            steps = steps + 1
            occupancy[pos] = steps

    return occupancy

def man_dist(x):
    return sum(map(abs, x))

def parse_input(input):
    return [(x[0], int(x[1:])) for x in input.split(',')]

def solve_part1(intersections):
    return sorted(list(map(man_dist, intersections)))[0]

def solve_part2(intersections, occA, occB):
    return sorted(list(map(lambda x : occA[x] + occB[x], intersections)))[0]


if __name__ == "__main__":
    with open("inputs/day3.txt") as f:
        linesA, linesB = map(parse_input, f.read().split('\n'))

        occA = build_occupancy_dict(linesA)
        occB = build_occupancy_dict(linesB)

        intersections = set(occA.keys()).intersection(set(occB.keys()))

        print(f"part1: {solve_part1(intersections)}")
        print(f"part1: {solve_part2(intersections, occA, occB)}")
