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

    output = np.array(digits, dtype=int)

    for _ in range(num_passes):
        np.dot(mtx, output, out=output)
        np.abs(output, out=output)
        np.mod(output, 10, out=output)

    return output
    
def solve_part2(offset, digits):
    buffer = list(itertools.islice(itertools.cycle(digits), 10000*len(digits)))
    assert offset >= len(buffer) / 2, "assumes offset >= half len buffer to exploit upper triangular mtx of 1's" 
    
    for _ in range(100):
        for i in range(len(buffer) - 2, offset - 1, -1):
            buffer[i] = abs(buffer[i] + buffer[i + 1]) % 10

    return int("".join(str(x) for x in buffer[offset:offset+8]))

if __name__ == "__main__":
    with open("inputs/day16.txt") as f:
        digits = [int(x) for x in f.read()]

        result = do_fft_passes(digits, 100)

        offset = int("".join(str(x) for x in digits[:7]))

        print(f"part1: {str().join(str(x) for x in result[:8])}")
        print(f"part2: {solve_part2(offset, digits)}")