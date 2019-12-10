import itertools

class interpreter:
    def __init__(self, mem):
        self.original_opcodes = mem.copy() 
        self.reset()

    def set_inputs(self, val):
        self.inputs = val

    def reset(self):
        self.pc = 0
        self.output = []
        self.inputs = []
        self.mem = self.original_opcodes.copy()
        self.halted = False
        self.relative_base = 0

    def _get_input(self): 
        inp = self.inputs[0]
        self.inputs = self.inputs[1:]
        return inp

    def _write_output(self, output):
        self.output.append(output)

    def _get_val(self, val, mode):
        if mode == 0:
            return self._read_mem(val)
        elif mode == 1:
            return val
        elif mode == 2:
            return self._read_mem(val + self.relative_base)
        
        raise ValueError(f"Bad addressing mode {mode}")

    def _ensure_mem_addr(self, addr):
        if addr < 0:
            raise ValueError(f"Address ({addr}) must be positive")
        if addr >= len(self.mem):
            self.mem.extend(itertools.repeat(0, addr - len(self.mem) + 1))

    def _write_mem(self, addr, v):
        self._ensure_mem_addr(addr)
        self.mem[addr] = v

    def _read_mem(self, addr):
        self._ensure_mem_addr(addr)
        return self.mem[addr]

    def _binary_op(self, fn, instr_modes):
        src0 = self._read_mem(self.pc + 0)
        src1 = self._read_mem(self.pc + 1)
        dest = self._read_mem(self.pc + 2)
        self.pc += 3
        self._write_mem(dest, fn(self._get_val(src0, instr_modes[0]), self._get_val(src1, instr_modes[1])))

    def _jump_op(self, test, instr_modes):
        src0 = self._read_mem(self.pc + 0)
        src1 = self._read_mem(self.pc + 1)
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
            packed_op = self.mem[self.pc]
            self.pc += 1

            op = packed_op % 100
            op_bits = int(packed_op / 100)

            instr_modes = tuple(map(lambda x : (op_bits // 10**x) % 10, range(3)))
 
            if op == 99:
                self.halted = True
                break
            elif op == 1:
                self._binary_op(lambda x, y : x + y, instr_modes)
            elif op == 2:
                self._binary_op(lambda x, y : x * y, instr_modes)
            elif op == 3:
                p0 = self._get_val(self._read_mem(self.pc), instr_modes[0])
                self.pc += 1
                self._write_mem(p0, self._get_input())
            elif op == 4:
                p0 = self._read_mem(self.pc)
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
            elif op == 9:
                p0 = self._get_val(self._read_mem(self.pc), instr_modes[0])
                self.pc += 1
                self.relative_base += p0 
            else:
                raise ValueError(f"Bad opcode {op}")


if __name__ == "__main__":
    with open("inputs/day9.txt") as f:
        opcodes = [int(x) for x in f.read().split(',')]
        interp = interpreter(opcodes)
        interp.set_inputs([1])
        interp.run()
        print(interp.output)
