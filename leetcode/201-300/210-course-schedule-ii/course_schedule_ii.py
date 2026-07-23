"""LeetCode 210 — Course Schedule II (Python mirror / oracle).

Kahn's topological sort recording the finish order; empty result on a cycle.
Seeds the queue in ascending course order and builds adjacency in pair order so
the emitted ordering matches the Kara version exactly. Mirrors the Kara version.
"""


def find_order(num_courses, prereqs):
    adj = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for a, b in prereqs:
        adj[b].append(a)
        indeg[a] += 1
    queue = [c for c in range(num_courses) if indeg[c] == 0]
    order = []
    head = 0
    while head < len(queue):
        node = queue[head]
        head += 1
        order.append(node)
        for nb in adj[node]:
            indeg[nb] -= 1
            if indeg[nb] == 0:
                queue.append(nb)
    return order if len(order) == num_courses else []


def report(num_courses, prereqs):
    order = find_order(num_courses, prereqs)
    if not order:
        print("impossible")
    else:
        print(" ".join(str(x) for x in order))


def main():
    report(1, [])
    report(2, [[1, 0]])
    report(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
    report(2, [[1, 0], [0, 1]])
    report(3, [[1, 0], [2, 1]])
    report(3, [[0, 1], [1, 2], [2, 0]])
    report(6, [[2, 5], [0, 5], [0, 4], [1, 4], [3, 2], [1, 3]])


main()
