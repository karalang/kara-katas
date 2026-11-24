# LeetCode #1319 bench, Python mirror of the Kāra bench: the ★ arm
# (union-find with halved paths and the smaller group hung under the
# larger) on 4 networks of 10^5 computers built once; then 25 passes, each
# moving one cable of every network to a pair chosen by the checksum so
# far, answering it and folding the answer plus the pass into the checksum.


def find(parent, x):
    at = x
    while parent[at] != at:
        parent[at] = parent[parent[at]]
        at = parent[at]
    return at


def make_connected(n, connections):
    if len(connections) < n - 1:
        return -1
    parent = list(range(n))
    size = [1] * n
    groups = n
    for c in connections:
        a = find(parent, c[0])
        b = find(parent, c[1])
        if a != b:
            big, small = (a, b) if size[a] >= size[b] else (b, a)
            parent[small] = big
            size[big] += size[small]
            groups -= 1
    return groups - 1


def main():
    n = 100000
    seed = 1319

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def wide(k):
        hi = next_random()
        return (hi * 32768 + next_random()) % k

    nets = []
    for kind in range(4):
        cables = []
        if kind == 1:
            cables = [[i - 1, i] for i in range(1, n)]
            for k in range(len(cables) - 1, 0, -1):
                j = wide(k + 1)
                cables[k], cables[j] = cables[j], cables[k]
        elif kind == 2:
            for g in range(n // 10):
                for u in range(10):
                    cables.append([10 * g + u, 10 * g + (u + 1) % 10])
        else:
            m = n if kind == 0 else n - 1
            while len(cables) < m:
                u = wide(n)
                v = wide(n)
                if u != v:
                    cables.append([u, v])
        nets.append(cables)
    check = 0
    for p in range(25):
        for t in range(4):
            cables = nets[t]
            m = len(cables)
            u = check % n
            v = (u + 1 + (check // 7) % (n - 1)) % n
            cables[check % m] = [u, v]
            got = make_connected(n, cables)
            check = (check * 31 + got + 1 + p) % 1000000007
    print(f"25 passes over 4 networks of 10^5: checksum {check}")


main()
