import re
import collections
import math
node_input = collections.namedtuple('node_input', 'id cost') 

class node:
    def __init__(self, inputs, output_count):
        self.inputs = inputs
        self.output_count = output_count
        self.leftover = 0

def topo_sort(graph):
    seen = set(['ORE'])
    sort_order = []

    def dfs(node_id):
        if node_id in seen:
            return

        node = graph[node_id]
        for inp_id, _ in node.inputs:
            if inp_id in seen:
                continue
            dfs(inp_id)

        sort_order.append(node_id)
        seen.add(node_id)

    dfs('FUEL')

    assert len(sort_order) == len(graph), "topo sort fail"
    return reversed(sort_order)

def build_graph(f):
    rgx = re.compile(r"(\d+ [A-Z]+)")
    graph = dict()

    for i, o in (tuple(x.split('=')) for x in f.readlines()):
        def parse(entry):
            (count, name) = entry.split(' ')
            return node_input(name, int(count))

        inputs = [ parse(x) for x in rgx.findall(i) ]
        output = parse(rgx.findall(o)[0])

        graph[output.id] = node(inputs, output.cost)

    return graph


def solve_part1(graph, sort_order):
    total_required = collections.defaultdict(int)
    total_required['FUEL'] = 1

    ore = 0

    for node_id in sort_order:
        node = graph[node_id]
        mul = math.ceil(total_required[node_id] / node.output_count)
        for inp_id, inp_cost in node.inputs:
            if inp_id == 'ORE':
                ore += inp_cost * mul
            else:
                total_required[inp_id] += inp_cost * mul

    return ore
    
if __name__ == "__main__":
    with open("inputs/day14.txt") as f:
        graph = build_graph(f)
        sort_order = topo_sort(graph)
        print(f"part1: {solve_part1(graph, sort_order)}")