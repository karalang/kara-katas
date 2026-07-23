"""LeetCode 207 — Course Schedule (Python mirror / oracle).

Kahn's topological sort: model each pair [a, b] as edge b->a, track in-degrees,
drain in-degree-0 nodes through a FIFO. Acyclic iff every course finishes.
Mirrors the Kara version.
"""


def can_finish(num_courses, prereqs):
    adj = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for a, b in prereqs:
        adj[b].append(a)
        indeg[a] += 1
    queue = [c for c in range(num_courses) if indeg[c] == 0]
    head = 0
    finished = 0
    while head < len(queue):
        node = queue[head]
        head += 1
        finished += 1
        for nb in adj[node]:
            indeg[nb] -= 1
            if indeg[nb] == 0:
                queue.append(nb)
    return finished == num_courses


def report(num_courses, prereqs):
    print("true" if can_finish(num_courses, prereqs) else "false")


def main():
    report(1, [])
    report(2, [[1, 0]])
    report(2, [[1, 0], [0, 1]])
    report(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
    report(3, [[0, 1], [1, 2], [2, 0]])
    report(5, [[1, 0], [2, 1], [3, 2], [4, 3]])
    report(3, [])


main()
