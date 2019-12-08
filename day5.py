import itertools

class interpreter:
    def __init__(self, opcodes):
        self.pc = 0
        self.opcodes = opcodes
        self.original_opcodes = opcodes.copy() 

    def set_input(self, val):
        self.input = val

    def reset(self, ):
        self.pc = 0
        self.output = None
        self.input = None
        self.opcodes = self.original_opcodes.copy()

    def _get_val(self, val, mode):
        return val if mode else self.opcodes[val]

    def _binary_op(self, fn, instr_modes):
        src0 = self.opcodes[self.pc + 0]
        src1 = self.opcodes[self.pc + 1]
        dest = self.opcodes[self.pc + 2]
        self.pc += 3
        self.opcodes[dest] = fn(self._get_val(src0, instr_modes[0]), self._get_val(src1, instr_modes[1]))

    def _jump_op(self, test, instr_modes):
        src0 = self.opcodes[self.pc + 0]
        src1 = self.opcodes[self.pc + 1]
        p0 = self._get_val(src0, instr_modes[0])
        p1 = self._get_val(src1, instr_modes[1])
        if test(p0):
            self.pc = p1
        else:
            self.pc += 2
        
    def run(self):
        while(True):
            packed_op = self.opcodes[self.pc]
            self.pc += 1

            op = packed_op % 100
            op_bits = int(packed_op / 100)

            instr_modes = tuple(map(lambda x : bool(int(op_bits / 10**x) % 10), range(3)))
 
            if op == 99:
                break
            elif op == 1:
                self._binary_op(lambda x, y : x + y, instr_modes)
            elif op == 2:
                self._binary_op(lambda x, y : x * y, instr_modes)
            elif op == 3:
                p0 = self.opcodes[self.pc]
                self.pc += 1
                self.opcodes[p0] = self.input
            elif op == 4:
                p0 = self.opcodes[self.pc]
                self.pc += 1
                output =  self._get_val(p0, instr_modes[0])
                print(f"output: {output}")
                self.output = self._get_val(p0, instr_modes[0])
            elif op == 5:
                self._jump_op(lambda x : x != 0, instr_modes)
            elif op == 6:
                self._jump_op(lambda x : x == 0, instr_modes)
            elif op == 7:
                self._binary_op(lambda x, y : 1 if x < y else 0, instr_modes)
            elif op == 8:
                self._binary_op(lambda x, y : 1 if x == y else 0, instr_modes)
            else:
                raise ValueError(f"Bad opcode {op}")

def solve_part1(interp):
    interp.set_input(1)
    interp.run()
    return interp.output

def solve_part2(interp):
    interp.set_input(5)
    interp.run()
    return interp.output

if __name__ == "__main__":
    with open("inputs/day5.txt") as f:
        opcodes = [int(x) for x in f.read().split(',')]
        interp = interpreter(opcodes)

        print(f"part1: {solve_part1(interp)}")

        interp.reset()

        print(f"part2: {solve_part2(interp)}")

        
