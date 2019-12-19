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

    def _get_param_addrs(self, addr_mode, count):
        d = { 0 : lambda x : self._read_mem(x), 1 : lambda x : x, 2 : lambda x : self._read_mem(x) + self.relative_base }
        l = [ d[addr_mode[i]](self.pc + i) for i in range(count) ]
        self.pc += count
        return l

    def _binary_op(self, fn, instr_modes):
        params = self._get_param_addrs(instr_modes, 3)
        self._write_mem(params[2], fn(self._read_mem(params[0]), self._read_mem(params[1])))

    def _jump_op(self, test, instr_modes):
        params = [self._read_mem(x) for x in self._get_param_addrs(instr_modes, 2)]
        if test(params[0]):
            self.pc = params[1]

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
            op_bits = packed_op // 100

            instr_modes = [(op_bits // 10**x) % 10 for x in range(3)]
            assert all(x in range(3) for x in instr_modes), "Bad instruction mode."
 
            if op == 99:
                self.halted = True
                break
            elif op == 1:
                self._binary_op(lambda x, y : x + y, instr_modes)
            elif op == 2:
                self._binary_op(lambda x, y : x * y, instr_modes)
            elif op == 3:
                params = self._get_param_addrs(instr_modes, 1)
                self._write_mem(params[0], self._get_input())
            elif op == 4:
                params = self._get_param_addrs(instr_modes, 1)
                self._write_output(self._read_mem(params[0]))
            elif op == 5:
                self._jump_op(lambda x : x != 0, instr_modes)
            elif op == 6:
                self._jump_op(lambda x : x == 0, instr_modes)
            elif op == 7:
                self._binary_op(lambda x, y : 1 if x < y else 0, instr_modes)
            elif op == 8:
                self._binary_op(lambda x, y : 1 if x == y else 0, instr_modes)
            elif op == 9:
                params = self._get_param_addrs(instr_modes, 1)
                self.relative_base += self._read_mem(params[0]) 
            else:
                raise ValueError(f"Bad opcode {op}")


if __name__ == "__main__":
    with open("inputs/day9.txt") as f:
        opcodes = [int(x) for x in f.read().split(',')]
        interp = interpreter(opcodes)
        interp.set_inputs([1])
        interp.run()
        print(interp.output)
