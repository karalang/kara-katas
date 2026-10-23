# LeetCode #913: Cat and Mouse -- bench: Python mirror of the retrograde
# analysis with a queue in cat_mouse_game.kara.


def cat_mouse_game(graph):
    n = len(graph)
    result = [0] * (n * n * 2)
    left = [0] * (n * n * 2)
    for m in range(n):
        for c in range(1, n):
            left[(m * n + c) * 2] = len(graph[m])
            moves = 0
            for d in graph[c]:
                if d != 0:
                    moves += 1
            left[(m * n + c) * 2 + 1] = moves
    queue = []
    for c in range(1, n):
        for t in range(2):
            result[c * 2 + t] = 1
            queue.append(c * 2 + t)
            result[(c * n + c) * 2 + t] = 2
            queue.append((c * n + c) * 2 + t)
    head = 0
    while head < len(queue):
        s = queue[head]
        head += 1
        t = s % 2
        c = s // 2 % n
        m = s // 2 // n
        won = result[s]
        if t == 1:
            for pm in graph[m]:
                p = (pm * n + c) * 2
                if result[p] == 0:
                    if won == 1:
                        result[p] = 1
                        queue.append(p)
                    else:
                        left[p] -= 1
                        if left[p] == 0:
                            result[p] = 2
                            queue.append(p)
        else:
            for pc in graph[c]:
                if pc != 0:
                    p = (m * n + pc) * 2 + 1
                    if result[p] == 0:
                        if won == 2:
                            result[p] = 2
                            queue.append(p)
                        else:
                            left[p] -= 1
                            if left[p] == 0:
                                result[p] = 1
                                queue.append(p)
    return result[(n + 2) * 2]


seed = 913


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_graph(n, per):
    adj = [False] * (n * n)
    for u in range(n):
        for v in range(u + 1, n):
            chance = per // 4 if u == 0 else per
            if next_random() % 1000 < chance:
                adj[u * n + v] = True
                adj[v * n + u] = True
    for v in range(1, n):
        alone = True
        for u in range(1, n):
            if adj[v * n + u]:
                alone = False
        if alone:
            u = 1 + next_random() % (n - 2)
            if u >= v:
                u += 1
            adj[u * n + v] = True
            adj[v * n + u] = True
    hole_alone = True
    for u in range(1, n):
        if adj[u]:
            hole_alone = False
    if hole_alone:
        u = 1 + next_random() % (n - 1)
        adj[u] = True
        adj[u * n] = True
    return [[u for u in range(n) if adj[v * n + u]] for v in range(n)]


def main():
    rounds = 4000
    wins = [0, 0, 0]
    check = 0
    for r in range(rounds):
        per = 20 if r % 4 == 0 else 60 if r % 4 == 1 else 150 if r % 4 == 2 else 400
        outcome = cat_mouse_game(random_graph(50, per))
        wins[outcome] += 1
        check = (check * 7 + outcome) % 1000000007
    print(f"{rounds} graphs of 50 nodes: {wins[0]} draws, {wins[1]} mouse wins, {wins[2]} cat wins, checksum {check}")


main()
