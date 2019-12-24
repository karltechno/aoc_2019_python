import collections
import itertools
import sys
import os
import numpy as np
import copy

class interpreter:
    def __init__(self, mem):
        self.original_opcodes = mem.copy() 
        self.reset()        
        
    def copy(self):
        return copy.deepcopy(self)

    def add_input(self, val):
        self.inputs.append(val)

    def reset(self):
        self.pc = 0
        self.inputs = collections.deque()
        self.mem = self.original_opcodes.copy()
        self.halted = False
        self.relative_base = 0

    def _get_input(self): 
        return self.inputs.popleft()

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
                raise StopIteration()
            elif op == 1:
                self._binary_op(lambda x, y : x + y, instr_modes)
            elif op == 2:
                self._binary_op(lambda x, y : x * y, instr_modes)
            elif op == 3:
                params = self._get_param_addrs(instr_modes, 1)
                self._write_mem(params[0], self._get_input())
            elif op == 4:
                params = self._get_param_addrs(instr_modes, 1)
                yield self._read_mem(params[0])
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


class bfs_node:
    def __init__(self, interp, cur_pos, steps):
        self.steps = steps
        self.pos = cur_pos
        self.interp = interp.copy()

def solve_part1(interp):
    visited = set()
    visited.add((0, 0))

    q = collections.deque()
    q.append(bfs_node(interp, (0, 0), 0))

    compass_to_tuple = { 1 : (0, 1), 2 : (0, -1), 3 : (-1, 0), 4 : (1, 0) }

    while True:
        entry = q.popleft()

        for k, v in compass_to_tuple.items():
            potential_pos = np.add(entry.pos, v)
            if tuple(potential_pos) in visited:
                continue

            visited.add(tuple(potential_pos))

            new_node = copy.deepcopy(entry)
            new_node.pos = potential_pos
            new_node.steps += 1
            new_node.interp.add_input(k)
            result = next(new_node.interp.run())
            if result == 0:
                continue
            if result == 1:
                q.append(new_node)
            if result == 2:
                return new_node.steps
            

if __name__ == "__main__":
    with open("inputs/day15.txt") as f:
        opcodes = [int(x) for x in f.read().split(',')]
        interp = interpreter(opcodes)
        print(f"part1: {solve_part1(interp)}")

