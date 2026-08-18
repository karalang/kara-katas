#!/usr/bin/env python3
"""LeetCode 283 — differential harness. Mirror of differential.kara.

The answer is unique, so equality is the oracle; the follow-up's "minimize
operations" is measured as a write count per solver.
"""


def cursor(a, st):
    write = 0
    for i in range(len(a)):
        if a[i] != 0:
            a[write] = a[i]
            st[0] += 1
            write += 1
    while write < len(a):
        a[write] = 0
        st[0] += 1
        write += 1


def swap_cursor(a, st):
    write = 0
    for i in range(len(a)):
        if a[i] != 0:
            if i != write:
                a[write], a[i] = a[i], a[write]
                st[0] += 2
            write += 1


def by_definition(a, st):
    out = [v for v in a if v != 0]
    while len(out) < len(a):
        out.append(0)
    for j in range(len(a)):
        a[j] = out[j]
        st[0] += 1


def nonzero_order_kept(src, res):
    return [v for v in src if v != 0] == [v for v in res if v != 0]


def zeros_all_at_end(res):
    seen = False
    for v in res:
        if v == 0:
            seen = True
        elif seen:
            return False
    return True


def main():
    cases = cursor_vs_stable = swap_vs_stable = 0
    multiset_broken = order_broken = zeros_misplaced = 0
    cursor_stores = swap_stores = swap_cheaper = cursor_cheaper = digest = 0

    for ln in range(0, 7):
        for code in range(4 ** ln):
            src = []
            m = code
            for _ in range(ln):
                pick = m % 4
                m //= 4
                src.append(0 if pick < 2 else (1 if pick == 2 else 2))

            a, b, c = list(src), list(src), list(src)
            wa, wb, wc = [0], [0], [0]
            cursor(a, wa)
            swap_cursor(b, wb)
            by_definition(c, wc)

            if a != c:
                cursor_vs_stable += 1
            if b != c:
                swap_vs_stable += 1
            if sorted(src) != sorted(a) or sorted(src) != sorted(b) or sorted(src) != sorted(c):
                multiset_broken += 1
            if not (nonzero_order_kept(src, a) and nonzero_order_kept(src, b)
                    and nonzero_order_kept(src, c)):
                order_broken += 1
            if not (zeros_all_at_end(a) and zeros_all_at_end(b) and zeros_all_at_end(c)):
                zeros_misplaced += 1

            cursor_stores += wa[0]
            swap_stores += wb[0]
            if wb[0] < wa[0]:
                swap_cheaper += 1
            if wa[0] < wb[0]:
                cursor_cheaper += 1
            for v in c:
                digest = (digest * 131 + v + 1) % 1000000007
            cases += 1

    print(f"cases {cases}")
    print(f"total writes: cursor {cursor_stores}, swap {swap_stores}")
    print(f"cases where swap wrote less {swap_cheaper}, where the cursor wrote less {cursor_cheaper}")
    print(f"digest {digest}")
    print(f"multiset broken {multiset_broken}, non-zero order broken {order_broken}, zeros misplaced {zeros_misplaced}")
    print(f"cursor vs definition {cursor_vs_stable}, swap vs definition {swap_vs_stable}")


main()
