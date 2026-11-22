# LeetCode #2876: Count Visited Nodes in a Directed Graph -- the bench,
# as visited.kara: 20 graphs of 10^5 nodes, each answered 20 times by
# the peeling arm.


def count_visited_nodes(edges):
    n = len(edges)
    incoming = [0] * n
    for e in edges:
        incoming[e] += 1
    peeled = [u for u in range(n) if incoming[u] == 0]
    head = 0
    while head < len(peeled):
        w = edges[peeled[head]]
        head += 1
        incoming[w] -= 1
        if incoming[w] == 0:
            peeled.append(w)
    answer = [0] * n
    for start in range(n):
        if incoming[start] > 0 and answer[start] == 0:
            cycle = [start]
            u = edges[start]
            while u != start:
                cycle.append(u)
                u = edges[u]
            for v in cycle:
                answer[v] = len(cycle)
    for u in reversed(peeled):
        answer[u] = answer[edges[u]] + 1
    return answer


seed = 2876


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count, rounds, n = 20, 20, 100000
    graphs = []
    for c in range(count):
        if c % 2 == 1:
            graphs.append([(i + next_random() % 5 + 1) % n for i in range(n)])
        else:
            graphs.append([(i + wide() % (n - 1) + 1) % n for i in range(n)])
    total = 0
    check = 0
    for r in range(rounds):
        for edges in graphs:
            counts = count_visited_nodes(edges)
            total += sum(counts)
            check = (check * 31 + counts[r] + counts[n - 1 - r]) % 1000000007
    print(f"{count} graphs of {n}, {rounds} rounds: visits total {total}, checksum {check}")


main()
