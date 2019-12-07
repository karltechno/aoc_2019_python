
class interpreter:
    def __init__(self, opcodes):
        self.pc = 0
        self.opcodes = opcodes
        self.original_opcodes = opcodes.copy() 

    def reset(self, ):
        self.pc = 0
        self.opcodes = self.original_opcodes.copy()

    def _binary_op(self, fn):
        src0 = self.opcodes[self.pc + 1]
        src1 = self.opcodes[self.pc + 2]
        dest = self.opcodes[self.pc + 3]
        self.pc += 4
        self.opcodes[dest] = fn(self.opcodes[src0], self.opcodes[src1])

    def solve_part1(self):
        self.opcodes[1] = 12
        self.opcodes[2] = 2
        self.run()
        return self.opcodes[0]

    def _run_part2(self, x, y):
        self.opcodes[1] = x
        self.opcodes[2] = y
        self.run()
        return self.opcodes[0]

    def solve_part2(self):
        self.reset()
        for x in range(100):
            for y in range(100):
                if self._run_part2(x, y) == 19690720:
                    return 100 * x + y
                self.reset()

        raise ArithmeticError("Failed to compute part2 result")

    def run(self):
        while(True):
            op = self.opcodes[self.pc]
            if op == 99:
                break
            elif op == 1:
                self._binary_op(lambda x, y : x + y)
            elif op == 2:
                self._binary_op(lambda x, y : x * y)


if __name__ == "__main__":
    with open("inputs/day2.txt") as f:
        opcodes = [int(x) for x in f.read().split(',')]
        interp = interpreter(opcodes)
        part1 = interp.solve_part1()
        part2 = interp.solve_part2()

        print(f"part1: {part1}") 
        print(f"part2: {part2}") 
