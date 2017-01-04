import sys
import unittest

def edmonds_karp(paths, entrance, exit):
    residuals = [0]*len(paths)
    for i, p in enumerate(paths):
        residuals[i] = list(p)
    bunny_count = 0
    flows = []
    for i in xrange(len(paths)):
        flows.append([0] * len(paths))

    while bunny_count < 2000000:
        new_count, path = bfs(paths, residuals, entrance, exit, flows)
        if not new_count:
            return bunny_count
        bunny_count += new_count
        node = exit
        while node != entrance:
            prev = path[node]
            flows[prev][node] += new_count
            flows[node][prev] -= new_count
            residuals[prev][node] -= new_count
            residuals[node][prev] += new_count
            node = prev
    return 2000000

def bfs(paths, residuals, entrance, exit, flows):
    path = [-1] * len(paths)

    path[entrance] = -2
    path_capacity = [0]*len(paths)
    path_capacity[entrance] = sys.maxint

    q = [entrance]
    while q:
        node = q.pop(0)
        for i in range(0, len(paths)):
            if i == node:
                continue
            if residuals[node][i] > 0 and path[i] == -1:
                path[i] = node
                path_capacity[i] = min(path_capacity[node],
                                       paths[node][i] - flows[node][i])
                if i == exit:
                    return (path_capacity[i], path)
                q.append(i)
    return (0, path)

def consolidate_entrances(entrances, paths):
    if len(entrances) == 1:
        return entrances[0]
    source_row = [0]*len(paths)
    entrance_total = sum(map(lambda entrance: sum(paths[entrance]), entrances))
    for e in entrances:
        source_row[e] = entrance_total
    paths.append(source_row)
    for p in paths:
        p.append(0)
    return len(paths) - 1

def consolidate_exits(exits, paths):
    if len(exits) == 1:
        return exits[0]
    exit_row = [0]*len(paths)
    exit_total = 0
    for e in exits:
        for p in paths:
            exit_total += p[e]
    paths.append(exit_row)
    for p in paths:
        p.append(0)
    for e in exits:
        paths[e][-1] = exit_total
    return len(paths) - 1

def answer(entrances, exits, paths):
    entrance = consolidate_entrances(entrances, paths)
    exit = consolidate_exits(exits, paths)
    return edmonds_karp(paths, entrance, exit)

class TestEdmondsKarp(unittest.TestCase):
    def test_karp(self):
        self.assertEqual(16, answer([0, 1], [4, 5], [
            [0, 0, 4, 6, 0, 0],
            [0, 0, 5, 2, 0, 0],
            [0, 0, 0, 0, 4, 4],
            [0, 0, 0, 0, 6, 6],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]))

        self.assertEqual(12, answer([0, 1], [4], [
            [0, 0, 4, 6, 0],
            [0, 0, 4, 6, 0],
            [0, 0, 0, 0, 6],
            [0, 0, 0, 0, 6],
            [0, 0, 0, 0, 0]
        ]))

        self.assertEqual(10, answer([0], [3], [
            [0, 4, 6, 0],
            [0, 0, 0, 6],
            [0, 0, 0, 6],
            [0, 0, 0, 0]
        ]))
