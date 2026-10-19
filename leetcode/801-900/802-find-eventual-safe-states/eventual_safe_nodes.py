# LeetCode 802 -- Find Eventual Safe States: mirrors the harness of
# eventual_safe_nodes.kara with the ★ arm's three-colour search.
import sys

sys.setrecursionlimit(100000)
seed = 802


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def eventual_safe_nodes(graph):
    n = len(graph)
    # 0 not seen yet, 1 grey (on the search or unsafe), 2 black (safe).
    colour = [0] * n

    def is_safe(node):
        if colour[node] != 0:
            return colour[node] == 2
        colour[node] = 1
        for nxt in graph[node]:
            if not is_safe(nxt):
                return False
        colour[node] = 2
        return True

    return [node for node in range(n) if is_safe(node)]


def text_list(lst):
    return "[" + ", ".join(str(v) for v in lst) + "]"


def text(graph):
    return "[" + ", ".join(text_list(out) for out in graph) + "]"


def show(graph):
    print(f"{text(graph)} -> {text_list(eventual_safe_nodes(graph))}")


def main():
    show([[1, 2], [2, 3], [5], [0], [5], [], []])
    show([[1, 2, 3, 4], [1, 2], [3, 4], [0, 4], []])
    show([[]])
    show([[0]])
    show([[1], [2], [0, 3], []])
    show([[1], [2], [3], [4], []])
    show([[1, 2], [3], [3], [3]])
    count = 0
    check = 0
    for i in range(300):
        n = 1 + next_random() % 40
        chance = 1 + next_random() % 4
        graph = []
        for _ in range(n):
            out = []
            for b in range(n):
                if next_random() % (2 * n) < chance:
                    out.append(b)
            graph.append(out)
        safe = eventual_safe_nodes(graph)
        count += len(safe)
        for v in safe:
            check = (check * 131 + v + 1) % 1000000007
        check = (check * 131 + i) % 1000000007
    print(f"300 random graphs: {count} safe nodes, checksum {check}")


main()
