import collections
import itertools
import sys
import os
import numpy as np


class interpreter:
    def __init__(self, mem):
        self.input_fn = None
        self.output_fn = None
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
        if self.input_fn is not None:
            return self.input_fn()

        inp = self.inputs[0]
        self.inputs = self.inputs[1:]
        return inp

    def _write_output(self, output):
        if self.output_fn:
            self.output_fn(output)

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

class day13():
    def __init__(self, interp):
        self.interp = interp
        self.grid = collections.defaultdict(int)
        self.output_id = 0
        self.next_coord = [0, 0]
        self.score = 0
        self.ball_pos = (0, 0)
        self.paddle_pos = (0, 0)

    def solve_part1(self):
        self.interp.output_fn = self.handle_output
        self.interp.run()
        return sum(int(x == 2) for x in self.grid.values())

    def solve_part2(self):
        self.interp.reset()
        self.interp.mem[0] = 2
        self.interp.input_fn = self.handle_input
        self.interp.run()
        print(self.score)

    def handle_input(self):
        return np.sign((self.ball_pos[0] - self.paddle_pos[0]))

    def _paint(self):
        grid_max = [0]*2
        for i in range(2):
            grid_max[i] = max(x[i] for x in self.grid.keys()) + 1

        raster_grid = [[0]*grid_max[0] for _ in range(grid_max[1])]
 
        for k,v in self.grid.items():
            raster_grid[k[1]][k[0]] = v

        os.system('cls' if os.name == 'nt' else 'clear')

        draw_dict = {0 : ' ', 1 : '#', 2 : '~', 3 : '_', 4 : '*'}
        for row in raster_grid:
            print("".join(draw_dict[x] for x in row))

        print(f'score: {self.score}')

    def handle_output(self, val):
        if self.output_id == 0:
            self.next_coord[0] = val
        elif self.output_id == 1:
            self.next_coord[1] = val
        elif self.output_id == 2:
            if self.next_coord == [-1, 0]:
                self.score = val
            else:
                pos = tuple(self.next_coord)
                self.grid[pos] = val
                if val == 4:
                    self.ball_pos = pos
                elif val == 3:
                    self.paddle_pos = pos

        self.output_id = (self.output_id + 1) % 3

if __name__ == "__main__":
    with open("inputs/day13.txt") as f:
        opcodes = [int(x) for x in f.read().split(',')]
        interp = interpreter(opcodes)
        d = day13(interp)
        print(f"part1: {d.solve_part1()}")
        print(f"part2: {d.solve_part2()}")
