# LeetCode 818 — Race Car, the best run to each distance.
#
# Mirrors racecar.kara: for a target t with n bits, either drive to
# 2^n - 1 and reverse, or stop at 2^(n-1) - 1, reverse, back up m
# accelerations, reverse again and cover the rest. O(t log t).


def racecar(target):
    best = [0] * (target + 1)
    for t in range(1, target + 1):
        n = t.bit_length()
        full = (1 << n) - 1
        if t == full:
            best[t] = n
            continue
        shortest = n + 1 + best[full - t]
        short = (1 << (n - 1)) - 1
        for m in range(n - 1):
            back = (1 << m) - 1
            steps = (n - 1) + 1 + m + 1 + best[t - short + back]
            if steps < shortest:
                shortest = steps
        best[t] = shortest
    return best[target]


def main():
    print(f"target = 3 -> {racecar(3)}")
    print(f"target = 6 -> {racecar(6)}")
    first = [racecar(t) for t in range(1, 33)]
    print(f"targets 1 to 32 -> [{', '.join(map(str, first))}]")
    for t in [10000, 9999, 8191, 8192, 4097, 5461]:
        print(f"target = {t} -> {racecar(t)}")
    seed = 818
    total = 0
    check = 0
    for _ in range(300):
        seed = (seed * 1103515245 + 12345) % 2147483648
        t = 1 + (seed // 65536) % 200
        answer = racecar(t)
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"300 random targets up to 200: total {total}, checksum {check}")


main()
