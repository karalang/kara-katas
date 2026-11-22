# LeetCode #2876: Count Visited Nodes in a Directed Graph -- the Python
# mirror of the ★ arm (visited.kara): the trees peeled off by in-degree,
# the cycles measured, the peeled nodes answered in reverse.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    global seed
    print(f"{show(count_visited_nodes([1, 2, 0, 0]))} {show(count_visited_nodes([1, 2, 3, 4, 0]))}")
    n = 100000
    ring = count_visited_nodes([(i + 1) % n for i in range(n)])
    path = count_visited_nodes([n - 2 if i == n - 1 else i + 1 for i in range(n)])
    print(f"{sum(ring)} {sum(path)} {path[0]} {path[n - 1]}")
    seed = 2876
    total = 0
    check = 0
    for c in range(3100):
        small = c < 3000
        n = next_random() % 7 + 2 if small else wide() % 99001 + 1000
        if not small and c % 2 == 1:
            edges = [(i + next_random() % 5 + 1) % n for i in range(n)]
        else:
            edges = [(i + wide() % (n - 1) + 1) % n for i in range(n)]
        for v in count_visited_nodes(edges):
            total += v
            check = (check * 31 + v) % 1000000007
        if c == 2999:
            print(f"3000 small graphs: visits total {total}, checksum {check}")
            total = 0
            check = 0
    print(f"100 large graphs: visits total {total}, checksum {check}")


main()
