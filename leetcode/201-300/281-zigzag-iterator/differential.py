#!/usr/bin/env python3
"""LeetCode 281 — differential harness. Mirror of differential.kara.

Two stateful iterators against the definition materialized round by round.
"""


def drain_cursor(lists):
    k = len(lists)
    cursor = [0] * k
    remaining = sum(len(v) for v in lists)
    turn = 0

    def settle(turn):
        tried = 0
        while tried < k:
            if cursor[turn] < len(lists[turn]):
                return turn
            turn = (turn + 1) % k
            tried += 1
        return turn

    turn = settle(turn)
    out = []
    while remaining > 0:
        t = turn
        out.append(lists[t][cursor[t]])
        cursor[t] += 1
        remaining -= 1
        turn = settle((t + 1) % k)
    return out


def drain_queue(lists):
    cursor = [0] * len(lists)
    queue = [i for i in range(len(lists)) if len(lists[i]) > 0]
    head = 0
    out = []
    while head < len(queue):
        t = queue[head]
        head += 1
        out.append(lists[t][cursor[t]])
        cursor[t] += 1
        if cursor[t] < len(lists[t]):
            queue.append(t)
    return out


def drain_eager(lists):
    longest = max((len(v) for v in lists), default=0)
    out = []
    for r in range(longest):
        for v in lists:
            if r < len(v):
                out.append(v[r])
    return out


def main():
    cases = cursor_vs_def = queue_vs_def = 0
    total_elements = with_empty_list = all_empty = digest = 0

    seed = 20260819
    for k in range(1, 6):
        for _ in range(300):
            lists = []
            any_empty = False
            every_empty = True
            for _ in range(k):
                seed = (seed * 1103515245 + 12345) % 2147483648
                ln = (seed // 17) % 7
                v = []
                for _ in range(ln):
                    seed = (seed * 1103515245 + 12345) % 2147483648
                    v.append(seed % 1000)
                if ln == 0:
                    any_empty = True
                else:
                    every_empty = False
                lists.append(v)
            if any_empty:
                with_empty_list += 1
            if every_empty:
                all_empty += 1

            a = drain_cursor(lists)
            b = drain_queue(lists)
            d = drain_eager(lists)
            if a != d:
                cursor_vs_def += 1
            if b != d:
                queue_vs_def += 1
            total_elements += len(d)
            for z, v in enumerate(d):
                digest = (digest * 131 + v * (z + 1)) % 1000000007
            cases += 1

    print(f"cases {cases}, elements interleaved {total_elements}")
    print(f"cases containing at least one EMPTY list {with_empty_list}")
    print(f"cases where every list is empty {all_empty}")
    print(f"digest {digest}")
    print(f"cursor vs the definition {cursor_vs_def}")
    print(f"queue  vs the definition {queue_vs_def}")


main()
