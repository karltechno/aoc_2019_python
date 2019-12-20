import itertools
import math

def simplify_angle(delta):
    gcd = math.gcd(abs(delta[0]), abs(delta[1]))
    return tuple(x // gcd for x in delta)

def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    num_active = len(iterables)
    nexts = itertools.cycle(iter(it).__next__ for it in iterables)
    while num_active:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            # Remove the iterator we just exhausted from the cycle.
            num_active -= 1
            nexts = itertools.cycle(itertools.islice(nexts, num_active))

def solve_part2(pos, asteroids):
    asteroids.remove(pos)
    deltas = [(tuple(x - y for x, y in zip(a, pos)), a) for a in asteroids]
    
    angle_dict = dict()

    for delta in deltas:
        simplified = simplify_angle(delta[0])
        if simplified in angle_dict:
            angle_dict[simplified].append(delta)
        else:
            angle_dict[simplified] = [delta] 

    for angle_list in angle_dict.values():
        angle_list.sort(key = lambda x : x[0][0]*x[0][0] + x[0][1]*x[0][1])

    calc_angle = lambda x : math.fmod(math.atan2(x[1], x[0]) + math.pi * 2.5, math.pi * 2)
    sorted_deltas = sorted(angle_dict.keys(), key = calc_angle)
    sorted_iters = (angle_dict[x] for x in sorted_deltas)

    rr = roundrobin(*sorted_iters)
    best = None
    for _ in range(200):
        best = next(rr)

    return best[1][0] * 100 + best[1][1]

if __name__ == "__main__":
    with open("inputs/day10.txt") as f:
        lines = [x.rstrip('\n') for x in f.readlines()]
        dims = (len(lines[0]), len(lines))

        entries = ( ((x, y), c) for y, line in enumerate(lines) for x, c in enumerate(line) )
        asteroids = set(x[0] for x in filter(lambda x : x[1] == '#', entries))
        
        best_count = 0
        best_pos = None

        for astr in asteroids:
            blocked_angles = set()
            num_seen = 0
            for coord in asteroids:
                if coord == astr:
                    continue

                delta = tuple(x[1] - x[0] for x in zip(astr, coord))
                angle = simplify_angle(delta)
                if angle in blocked_angles:
                    continue
                num_seen += 1
                blocked_angles.add(angle)

            if num_seen > best_count:
                best_count = num_seen
                best_pos = astr

        print(f"part1: {best_count}")
        print(f"part2: {solve_part2(best_pos, asteroids)}")