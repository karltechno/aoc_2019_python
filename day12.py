import re
import numpy as np
import itertools

def gcd(a,b):
    while b > 0:
        a, b = b, a % b
    return a
    
def lcm(a, b):
    return a * b // gcd(a, b)

class body():
    def __init__(self, pos):
        self.vel = np.array([0, 0, 0])
        self.pos = pos
        
def step_system(bodies):
    for pair in itertools.combinations(bodies, 2):
        delta_sign = np.sign(np.subtract(pair[1].pos, pair[0].pos))
        pair[0].vel = np.add(delta_sign, pair[0].vel)
        pair[1].vel = np.add(np.negative(delta_sign), pair[1].vel)

    for b in bodies:
        b.pos = np.add(b.pos, b.vel)

def solve_part1(bodies):
    for _ in range(1000):
        step_system(bodies)

    energy = 0

    for b in bodies:
        energy += sum(abs(x) for x in b.pos) * sum(abs(x) for x in b.vel)

    return energy

def solve_part2(bodies):
    history = [set(), set(), set()]

    collect_axis_state = lambda x : tuple(b.pos[x] for b in bodies) + tuple(b.vel[x] for b in bodies)
    initial_state = [collect_axis_state(i) for i in range(3)]
            
    iter = 0
    cycles = [-1, -1, -1]

    while -1 in cycles:
        step_system(bodies)
        iter += 1
        for i in range(3):
            state = collect_axis_state(i)
            if cycles[i] == -1 and state == initial_state[i]:
                cycles[i] = iter

    return lcm(cycles[0], lcm(cycles[1], cycles[2]))


if __name__ == "__main__":
    with open("inputs/day12.txt") as f:
        r = re.compile('(-?[0-9]+)')
        bodies = []
        for l in f.readlines():
            bodies.append(body([int(x) for x in r.findall(l)]))
        
        print(f"part1: {solve_part1(bodies.copy())}")
        print(f"part2: {solve_part2(bodies.copy())}")
