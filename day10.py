import itertools
import math

def simplify_angle(delta):
    gcd = math.gcd(abs(delta[0]), abs(delta[1]))
    return tuple(x // gcd for x in delta)

if __name__ == "__main__":
    with open("inputs/day10.txt") as f:
        lines = [x.rstrip('\n') for x in f.readlines()]
        dims = (len(lines[0]), len(lines))

        entries = ( ((x, y), c) for y, line in enumerate(lines) for x, c in enumerate(line) )
        asteroids = set(x[0] for x in filter(lambda x : x[1] == '#', entries))
        
        best_count = 0

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

            best_count = max(num_seen, best_count)

        print(f"part1: {best_count}")
