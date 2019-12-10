import itertools

class interpreter:
    def __init__(self, opcodes):
        self.original_opcodes = opcodes.copy() 
        self.reset()

    def set_inputs(self, val):
        self.inputs = val

    def reset(self):
        self.pc = 0
        self.output = None
        self.inputs = []
        self.opcodes = self.original_opcodes.copy()
        self.halted = False
        self.output_fn = None

    def _get_input(self): 
        inp = self.inputs[0]
        self.inputs = self.inputs[1:]
        return inp

    def _write_output(self, output):
        self.output = output
        if self.next_interp is not None:
            self.next_interp.run_with_input(output)

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

    def run_with_input(self, input):
        if self.halted:
            return
            
        self.inputs.append(input)
        self.run()
        
    def run(self):
        while(True):
            if self.halted:
                return

            packed_op = self.opcodes[self.pc]
            self.pc += 1

            op = packed_op % 100
            op_bits = int(packed_op / 100)

            instr_modes = tuple(map(lambda x : bool(int(op_bits / 10**x) % 10), range(3)))
 
            if op == 99:
                self.halted = True
                break
            elif op == 1:
                self._binary_op(lambda x, y : x + y, instr_modes)
            elif op == 2:
                self._binary_op(lambda x, y : x * y, instr_modes)
            elif op == 3:
                p0 = self.opcodes[self.pc]
                self.pc += 1
                self.opcodes[p0] = self._get_input()
            elif op == 4:
                p0 = self.opcodes[self.pc]
                self.pc += 1
                self._write_output(self._get_val(p0, instr_modes[0]))
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

def solve_part1(opcodes):
    best_output = -1
    interp = interpreter(opcodes)
    for phase in itertools.permutations(range(5), 5):
        next_input = 0
        for i in range(5):
            interp.reset()
            interp.set_inputs([phase[i], next_input])
            interp.run()
            next_input = interp.output

        best_output = max(next_input, best_output)
    
    return best_output

def solve_part2(opcodes):
    best_output = -1
    for phase in itertools.permutations(range(5, 10), 5):
        interps = []

        for i in range(5):
            interps.append(interpreter(opcodes))

        for i in range(5):
            interps[i].next_interp = interps[(i + 1) % 5]       
            interps[i].inputs.append(phase[i])

        interps[0].inputs.append(0)
    
        interps[0].run()

        best_output = max(best_output, interps[4].output)

    return best_output


if __name__ == "__main__":
    with open("inputs/day7.txt") as f:
        opcodes = [int(x) for x in f.read().split(',')]
        print(f"part1: {solve_part1(opcodes)}")
        print(f"part2: {solve_part2(opcodes)}")

