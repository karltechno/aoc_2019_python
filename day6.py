
def parse_line(graph, line, parent_dict):
    s = line.split(')')
    node = s[1].rstrip('\n')
    parent = s[0]
    if s[0] in graph:
        graph[parent].add(node)
    else:
        graph[parent] = { node }

    parent_dict[node] = parent

def dfs(graph, node_id, cur_depth, leaf_depths):
    leaf_depths.append(cur_depth)
    if node_id in graph:
        for v in graph[node_id]:
            dfs(graph, v, cur_depth + 1, leaf_depths)

def solve_part1(graph):
    leaf_depths = []
    dfs(graph, 'COM', 0, leaf_depths)
    return sum(leaf_depths)

    
def bfs(graph, node, to_find):
    q = [(node, 0)]
    seen = set()

    while True:
        (cur_node, cur_depth) = q[0]
        q.remove(q[0])

        if cur_node in graph:
            for v in graph[cur_node]:
                if v == to_find:
                    return cur_depth + 1
                elif v not in seen:
                    q.append((v, cur_depth + 1))
                    seen.add(v)

def solve_part2(graph, parent_dict):
    return bfs(graph, parent_dict['YOU'], parent_dict['SAN'])

if __name__ == "__main__":
    with open("inputs/day6.txt") as f:
        graph = dict()
        parents = dict()
        for line in f.readlines():
            parse_line(graph, line, parents)

        print(f"part1: {solve_part1(graph)}")

        for (k, v) in parents.items():
            if k in graph:
                graph[k].add(v)
            else:
                graph[k] = {v}

        print(f"part2: {solve_part2(graph, parents)}")
