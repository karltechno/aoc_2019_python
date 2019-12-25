import itertools

def fft_pass(digits):
    base_seq = [0, 1, 0, -1]
    output = []
    for i in range(len(digits)):
        seq = [y for x in base_seq for y in (x,)*(i+1)]
        iter = itertools.cycle(seq)
        next(iter)

        o = sum(x * y for x, y in zip(digits, iter))
        output.append(abs(o) % 10)

    return output

if __name__ == "__main__":
    with open("inputs/day16.txt") as f:
        digits = [int(x) for x in f.read()]


    for _ in range(100):
        digits = fft_pass(digits)

    print("part1: " + "".join(str(x) for x in digits[:8]))