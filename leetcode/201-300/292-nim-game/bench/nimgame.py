"""Benchmark twin for LeetCode #292 — same algorithm as nimgame.kara."""

N = 20000000


def main():
    win = bytearray(N + 1)
    for i in range(1, N + 1):
        w = 0
        for take in (1, 2, 3):
            if i - take >= 0 and not win[i - take]:
                w = 1
        win[i] = w
    losing = checksum = 0
    for i in range(N + 1):
        if not win[i]:
            losing += 1
            checksum = (checksum * 31 + i) % 1000000007
    print(f"losing {losing} checksum {checksum}")


if __name__ == "__main__":
    main()
