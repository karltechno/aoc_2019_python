import itertools
import numpy as np

def do_fft_passes(digits, num_passes):
    mtx = []
    base_seq = [0, 1, 0, -1]
    for i in range(len(digits)):
        seq = [y for x in base_seq for y in (x,)*(i+1)]
        iter = itertools.cycle(seq)
        next(iter)
        mtx.append([x for x in itertools.islice(iter, len(digits))])

    mtx = np.array(mtx, dtype=int)

    output = np.array(digits.copy(), dtype=int)

    for _ in range(num_passes):
        np.dot(mtx, output, out=output)
        np.abs(output, out=output)
        np.mod(output, 10, out=output)

    return output
    

if __name__ == "__main__":
    with open("inputs/day16.txt") as f:
        digits = [int(x) for x in f.read()]

    result = do_fft_passes(digits, 100)

    print("part1: " + "".join(str(x) for x in result[:8]))