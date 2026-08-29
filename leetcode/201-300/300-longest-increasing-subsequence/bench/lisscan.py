"""Benchmark mirror of lisscan.kara - LeetCode #300, Longest Increasing
Subsequence.

Same patience sorting, same hand-written binary search, same reused tails
buffer. Deliberately not using bisect - that would hand the inner loop to C and
measure something other than the algorithm. See ../README.md.
"""

N_ARRAYS = 3000
LEN = 512
PASSES = 24
SPREAD = 4096


def lcg(state: int) -> int:
    return (state * 1103515245 + 12345) & 0x7FFFFFFF


def main() -> None:
    total = N_ARRAYS * LEN
    data = [0] * total

    state = 20300
    for i in range(total):
        state = lcg(state)
        data[i] = (state // 65536) % SPREAD

    tails = [0] * LEN
    checksum = 0

    for _pass in range(PASSES):
        for a in range(N_ARRAYS):
            base = a * LEN
            n_tails = 0

            for k in range(LEN):
                x = data[base + k]

                lo, hi = 0, n_tails
                while lo < hi:
                    mid = lo + (hi - lo) // 2
                    if tails[mid] < x:
                        lo = mid + 1
                    else:
                        hi = mid

                if lo == n_tails:
                    tails[n_tails] = x
                    n_tails += 1
                else:
                    tails[lo] = x

            checksum = (checksum * 31 + n_tails) % 1000000007

    print(f"arrays {N_ARRAYS} len {LEN} passes {PASSES} checksum {checksum}")


if __name__ == "__main__":
    main()
