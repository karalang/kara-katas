"""Benchmark mirror of LeetCode #319 — the round simulation.

Same algorithm as bench/bulb_switcher.kara: PASSES passes, each simulating n
rounds over an n-bulb byte array and folding the count of lit bulbs together
with the sum of their indices."""

BULBS = 6000000
PASSES = 10
STRIDE = 90011
MASKMOD = 1073741823


def main() -> None:
    on = bytearray(BULBS + 1)

    sink = 0
    for p in range(PASSES):
        n = BULBS - p * STRIDE

        for b in range(n + 1):
            on[b] = 0

        for step in range(1, n + 1):
            for b in range(step, n + 1, step):
                on[b] ^= 1

        count = 0
        idx_sum = 0
        for b in range(1, n + 1):
            if on[b] == 1:
                count += 1
                idx_sum = (idx_sum + b) % MASKMOD
        sink = (sink * 31 + count * 7919 + idx_sum) % MASKMOD

    print(f"checksum {sink}")


if __name__ == "__main__":
    main()
