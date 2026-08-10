"""LeetCode 253 - differential harness. Python oracle.

Mirrors differential.kara exactly: same LCG, same small-coordinate pool, same
shuffle, the same three counters and the same census.

Times are drawn from 0..23 deliberately. The only shape the three counters can
differ on is a meeting ending exactly as another begins, and a wide coordinate
pool produces those too rarely to test anything -- see the README.
"""
from min_meeting_rooms import heap_push, heap_pop


def make_case(seed):
    state = seed
    out = []
    state = (state * 1103515245 + 12345) & 2147483647
    n = (state // 65536) % 11
    for _ in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        s = (state // 65536) % 24
        state = (state * 1103515245 + 12345) & 2147483647
        d = (state // 65536) % 6 + 1
        out.append((s, s + d))
    k = len(out) - 1
    while k > 0:
        state = (state * 1103515245 + 12345) & 2147483647
        swap = (state // 65536) % (k + 1)
        out[k], out[swap] = out[swap], out[k]
        k -= 1
    return out


def count_heap(iv):
    s = sorted(iv, key=lambda x: x[0])
    heap = []
    rooms = 0
    for x in s:
        while heap and heap[0] <= x[0]:
            heap_pop(heap)
        heap_push(heap, x[1])
        rooms = max(rooms, len(heap))
    return rooms


def count_sweep(iv):
    n = len(iv)
    if n == 0:
        return 0
    starts = sorted(x[0] for x in iv)
    ends = sorted(x[1] for x in iv)
    j = active = best = 0
    for k in range(n):
        while j < n and ends[j] <= starts[k]:
            active -= 1
            j += 1
        active += 1
        best = max(best, active)
    return best


def count_events(iv):
    n = len(iv)
    if n == 0:
        return 0
    events = []
    for x in iv:
        events.append((x[0], 1))
        events.append((x[1], -1))
    events.sort(key=lambda e: (e[0], e[1]))
    active = best = 0
    for e in events:
        active += e[1]
        best = max(best, active)
    return best


def main():
    cases = 1500
    seed = 253253
    mismatches = total_rooms = max_rooms = coincident = digest = 0

    for _ in range(cases):
        seed = (seed * 1103515245 + 12345) & 2147483647
        iv = make_case(seed)

        a = count_heap(iv)
        b = count_sweep(iv)
        d = count_events(iv)

        if a != b or a != d:
            mismatches += 1
        total_rooms += a
        max_rooms = max(max_rooms, a)
        digest = (digest * 131 + a) % 1000000007

        has = any(iv[x][1] == iv[y][0] for x in range(len(iv)) for y in range(len(iv)) if x != y)
        if has:
            coincident += 1

    print(f"cases {cases}")
    print(f"total rooms {total_rooms}")
    print(f"max rooms {max_rooms}")
    print(f"with coincident endpoints {coincident}")
    print(f"digest {digest}")
    print(f"mismatches {mismatches}")


if __name__ == "__main__":
    main()
