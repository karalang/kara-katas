"""LeetCode 295 benchmark lane — Python mirror of medianfinder.kara.

Runs the FULL 2M adds, same as the compiled lanes, and produces the same sink:
`adds 2000000 checksum 831081041`. No scale-down was needed — heapq is C-coded,
so this lane lands around 2.4s against the compiled lanes' ~0.4s rather than the
two orders of magnitude a hand-rolled Python heap would have cost.

That is also why this mirror uses heapq while the C, Rust and Go mirrors all
hand-roll: a Python-level sift loop would measure interpreter dispatch, not the
algorithm. The negation trick for the max-heap side is safe here because
Python's ints are unbounded — the Kara version avoids it precisely because
-i64.MIN overflows and Kara traps that (see median_finder.kara's header).
"""

import heapq

N = 2_000_000


def main():
    lo = []  # max-heap via negation: lower half
    hi = []  # min-heap: upper half
    state = 12345
    checksum = 0

    for _ in range(N):
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        v = state % 1000003 - 500000

        heapq.heappush(lo, -v)
        heapq.heappush(hi, -heapq.heappop(lo))
        if len(hi) > len(lo):
            heapq.heappush(lo, -heapq.heappop(hi))

        twice = -2 * lo[0] if len(lo) > len(hi) else -lo[0] + hi[0]
        checksum = (checksum * 31 + twice) % 1000000007

    print(f"adds {N} checksum {checksum}")


if __name__ == "__main__":
    main()
