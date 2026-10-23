# LeetCode #886 bench: Python mirror of possible_bipartition.kara (the ★
# arm, two colours by breadth-first search) on the same 4000 groups.

from collections import deque


def possible_bipartition(n, dislikes):
    adj = [[] for _ in range(n + 1)]
    for a, b in dislikes:
        adj[a].append(b)
        adj[b].append(a)
    colour = [-1] * (n + 1)
    queue = deque()
    for start in range(1, n + 1):
        if colour[start] >= 0:
            continue
        colour[start] = 0
        queue.append(start)
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if colour[v] < 0:
                    colour[v] = 1 - colour[u]
                    queue.append(v)
                elif colour[v] == colour[u]:
                    return False
    return True


seed = 886


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    yes = 0
    check = 0
    for _ in range(4000):
        # n people, each disliking the people five distinct offsets on,
        # every offset below n / 2 so that no pair repeats: 5n pairs, up
        # to 10^4; the offsets odd, but one of them even half the time
        n = 1000 + next_random() % 1001
        spoil = next_random() % 2 == 0
        offsets = []
        while len(offsets) < 5:
            d = 1 + next_random() % (n // 2 - 1)
            if d % 2 == 0 and not (spoil and len(offsets) == 0):
                d -= 1
            if d not in offsets:
                offsets.append(d)
        dislikes = []
        for a in range(n):
            for k in range(5):
                dislikes.append([a + 1, (a + offsets[k]) % n + 1])
        ok = possible_bipartition(n, dislikes)
        bit = 1 if ok else 0
        yes += bit
        check = (check * 3 + bit + 1) % 1000000007
    print(f"4000 groups of up to 2000 people: {yes} can be split, checksum {check}")


main()
