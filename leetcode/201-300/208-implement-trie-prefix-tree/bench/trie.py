"""Benchmark workload for LeetCode #208 — Implement Trie (Prefix Tree; Python scale lane)."""

ALPHA = 5


def main():
    nwords = 30000
    nquery = 8000000

    children = [0] * ALPHA  # root at index 0
    is_end = [0]

    state = 12345

    # Build phase.
    for _ in range(nwords):
        state = (state * 1103515245 + 12345) & 2147483647
        length = 2 + state % 7
        cur = 0
        for _ in range(length):
            state = (state * 1103515245 + 12345) & 2147483647
            c = state % ALPHA
            nxt = children[cur * ALPHA + c]
            if nxt == 0:
                idx = len(is_end)
                children.extend([0] * ALPHA)
                is_end.append(0)
                children[cur * ALPHA + c] = idx
                cur = idx
            else:
                cur = nxt
        is_end[cur] = 1

    # Query phase.
    sink = 0
    for _ in range(nquery):
        state = (state * 1103515245 + 12345) & 2147483647
        length = 2 + state % 7
        cur = 0
        alive = True
        for _ in range(length):
            state = (state * 1103515245 + 12345) & 2147483647
            c = state % ALPHA
            if alive:
                nxt = children[cur * ALPHA + c]
                if nxt == 0:
                    alive = False
                else:
                    cur = nxt
        if alive:
            sink += 1
            if is_end[cur] == 1:
                sink += 2

    print(sink)


main()
