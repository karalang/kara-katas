"""Build-once + punch Floyd two-phase cycle-entry detection over an index-pool of
K lists (LeetCode #142; Python scale lane). nxt[i] = next global index or -1
(see linked_list_cycle_ii.kara)."""


def detect(nxt, head):
    slow = head
    fast = head
    met = False
    while True:
        fast = nxt[fast]
        if fast < 0:
            return -1
        fast = nxt[fast]
        if fast < 0:
            return -1
        slow = nxt[slow]
        if slow == fast:
            met = True
            break
    if not met:
        return -1
    slow = head
    while slow != fast:
        slow = nxt[slow]
        fast = nxt[fast]
    return slow - head


def main():
    k_lists = 1000
    length = 60
    passes = 3000
    cycpct = 50
    pool = k_lists * length

    nxt = [0] * pool
    target = []
    tail = []

    state = 12345

    for k in range(k_lists):
        base = k * length
        for j in range(length - 1):
            nxt[base + j] = base + j + 1
        t = base + length - 1
        tail.append(t)

        state = (state * 1103515245 + 12345) & 2147483647
        coin = (state >> 16) % 100
        state = (state * 1103515245 + 12345) & 2147483647
        tl = (state >> 16) % length
        target.append(base + tl)

        if coin < cycpct:
            nxt[t] = base + tl
        else:
            nxt[t] = -1

    sink = 0
    for p in range(passes):
        idx = p % k_lists
        ti = tail[idx]
        if nxt[ti] < 0:
            nxt[ti] = target[idx]
        else:
            nxt[ti] = -1

        for kk in range(k_lists):
            e = detect(nxt, kk * length)
            sink += e + 1

    print(sink)


main()
